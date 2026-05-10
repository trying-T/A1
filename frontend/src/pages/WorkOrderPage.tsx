import { ReloadOutlined } from "@ant-design/icons";
import { Alert, Button, Card, Descriptions, List, Space, Table, Tag, Typography } from "antd";
import type { ColumnsType } from "antd/es/table";
import { useEffect, useState } from "react";

import { getWorkOrder, getWorkOrders } from "../api/workOrderApi";
import type { WorkOrderItem } from "../types/workOrder";

const { Text, Title, Paragraph } = Typography;

type WorkOrderPageProps = {
  selectedWorkOrderId?: string | null;
};

export default function WorkOrderPage({ selectedWorkOrderId }: WorkOrderPageProps) {
  const [items, setItems] = useState<WorkOrderItem[]>([]);
  const [selected, setSelected] = useState<WorkOrderItem | null>(null);
  const [loading, setLoading] = useState(true);
  const [detailLoading, setDetailLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    void refreshWorkOrders();
  }, [selectedWorkOrderId]);

  async function refreshWorkOrders() {
    setLoading(true);
    setError("");
    try {
      const result = await getWorkOrders();
      setItems(result.items);
      const nextSelected =
        result.items.find((item) => item.work_order_id === selectedWorkOrderId) ?? result.items[0] ?? null;
      if (nextSelected) {
        setSelected(nextSelected);
      } else {
        setSelected(null);
      }
    } catch (nextError) {
      setError(getErrorMessage(nextError));
    } finally {
      setLoading(false);
    }
  }

  async function openDetail(workOrderId: string) {
    setDetailLoading(true);
    setError("");
    try {
      const detail = await getWorkOrder(workOrderId);
      setSelected(detail);
    } catch (nextError) {
      setError(getErrorMessage(nextError));
    } finally {
      setDetailLoading(false);
    }
  }

  const columns: ColumnsType<WorkOrderItem> = [
    {
      title: "记录编号",
      dataIndex: "work_order_id",
      width: 160,
      render: (value: string) => <Text strong>{value}</Text>,
    },
    {
      title: "故障现象",
      dataIndex: "fault_symptom",
      ellipsis: true,
    },
    {
      title: "设备类型",
      dataIndex: "equipment_type",
      width: 140,
      render: (value?: string | null) => value || "未指定",
    },
    {
      title: "状态",
      dataIndex: "status",
      width: 100,
      render: (value: string) => <Tag color="processing">{value}</Tag>,
    },
    {
      title: "创建时间",
      dataIndex: "created_at",
      width: 190,
      render: (value: string) => formatDate(value),
    },
    {
      title: "操作",
      width: 100,
      render: (_, item) => (
        <Button type="link" onClick={() => void openDetail(item.work_order_id)}>
          查看
        </Button>
      ),
    },
  ];

  return (
    <Space direction="vertical" size={20} className="page-fill">
      {error ? <Alert type="error" showIcon message={error} /> : null}

      <Card
        title="检修记录列表"
        extra={
          <Button icon={<ReloadOutlined />} onClick={() => void refreshWorkOrders()}>
            刷新
          </Button>
        }
      >
        <Table
          rowKey="work_order_id"
          loading={loading}
          columns={columns}
          dataSource={items}
          pagination={false}
          scroll={{ x: 920 }}
          onRow={(record) => ({
            onClick: () => void openDetail(record.work_order_id),
          })}
        />
      </Card>

      <Card title="检修记录详情" loading={detailLoading}>
        {selected ? (
          <Space direction="vertical" size={20} className="page-fill">
            <Descriptions bordered column={1}>
              <Descriptions.Item label="记录编号">{selected.work_order_id}</Descriptions.Item>
              <Descriptions.Item label="设备类型">{selected.equipment_type || "未指定"}</Descriptions.Item>
              <Descriptions.Item label="故障现象">{selected.fault_symptom}</Descriptions.Item>
              <Descriptions.Item label="故障理解">{selected.fault_understanding}</Descriptions.Item>
              <Descriptions.Item label="状态">{selected.status}</Descriptions.Item>
              <Descriptions.Item label="创建时间">{formatDate(selected.created_at)}</Descriptions.Item>
              <Descriptions.Item label="操作备注">
                {selected.operator_note || "暂无"}
              </Descriptions.Item>
            </Descriptions>

            <DetailList title="可能原因" items={selected.possible_causes} />
            <DetailList title="排查步骤" items={selected.repair_steps} ordered />
            <DetailList title="安全注意事项" items={selected.safety_notes} />

            <Card type="inner" title="依据来源">
              {selected.sources.length === 0 ? (
                <Alert type="warning" showIcon message="该记录没有保存 sources。" />
              ) : (
                <List
                  dataSource={selected.sources}
                  renderItem={(source) => (
                    <List.Item>
                      <Space direction="vertical" size={4} className="page-fill">
                        <Text strong>{source.filename ?? source.document_title}</Text>
                        <Space wrap>
                          <Tag color="geekblue">score {source.score.toFixed(4)}</Tag>
                          {source.chunk_index !== null && source.chunk_index !== undefined ? (
                            <Tag>chunk {source.chunk_index}</Tag>
                          ) : null}
                        </Space>
                        <Text type="secondary">chunk_id: {source.chunk_id}</Text>
                        <Text type="secondary">document_id: {source.document_id}</Text>
                      </Space>
                    </List.Item>
                  )}
                />
              )}
            </Card>
          </Space>
        ) : (
          <Alert type="info" showIcon message="暂无检修记录，请先在检修问答页生成一条记录。" />
        )}
      </Card>
    </Space>
  );
}

function DetailList({ title, items, ordered = false }: { title: string; items: string[]; ordered?: boolean }) {
  const ListTag = ordered ? "ol" : "ul";
  return (
    <Card type="inner" title={title}>
      {items.length === 0 ? (
        <Text type="secondary">暂无内容。</Text>
      ) : (
        <ListTag className="result-list">
          {items.map((item, index) => (
            <li key={`${title}-${index}`}>
              <Paragraph>{item}</Paragraph>
            </li>
          ))}
        </ListTag>
      )}
    </Card>
  );
}

function formatDate(value: string) {
  const parsed = new Date(value);
  if (Number.isNaN(parsed.getTime())) {
    return value;
  }
  return parsed.toLocaleString("zh-CN", {
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
  });
}

function getErrorMessage(error: unknown) {
  return error instanceof Error ? error.message : "操作失败，请稍后重试。";
}
