import { RobotOutlined, SendOutlined } from "@ant-design/icons";
import { Alert, Button, Card, Collapse, Form, Input, List, Space, Tag, Typography, message } from "antd";
import { useState } from "react";

import { repairChat } from "../api/chatApi";
import { createWorkOrder } from "../api/workOrderApi";
import type { RepairChatResponse } from "../types/repairChat";

const { Text, Title, Paragraph } = Typography;
const { TextArea } = Input;

const DEFAULT_QUESTION = "设备启动后电源指示灯不亮，风扇也不转，应该如何排查？";

type RepairChatPageProps = {
  onWorkOrderCreated?: (workOrderId: string) => void;
};

export default function RepairChatPage({ onWorkOrderCreated }: RepairChatPageProps) {
  const [form] = Form.useForm<{ question: string; equipment_type?: string }>();
  const [result, setResult] = useState<RepairChatResponse | null>(null);
  const [lastRequest, setLastRequest] = useState<{ question: string; equipment_type?: string | null } | null>(null);
  const [loading, setLoading] = useState(false);
  const [creatingWorkOrder, setCreatingWorkOrder] = useState(false);
  const [error, setError] = useState("");

  async function handleSubmit(values: { question: string; equipment_type?: string }) {
    setLoading(true);
    setError("");
    try {
      const response = await repairChat({
        question: values.question.trim(),
        equipment_type: values.equipment_type?.trim() || null,
        top_k: 5,
      });
      setLastRequest({
        question: values.question.trim(),
        equipment_type: values.equipment_type?.trim() || null,
      });
      setResult(response);
    } catch (nextError) {
      setError(nextError instanceof Error ? nextError.message : "RAG 问答请求失败，请稍后重试。");
    } finally {
      setLoading(false);
    }
  }

  async function handleCreateWorkOrder() {
    if (!result || !lastRequest) {
      message.warning("请先生成一条检修建议。");
      return;
    }

    setCreatingWorkOrder(true);
    try {
      const workOrder = await createWorkOrder({
        equipment_type: lastRequest.equipment_type,
        fault_symptom: lastRequest.question,
        fault_understanding: result.fault_understanding,
        possible_causes: result.possible_causes,
        repair_steps: result.repair_steps,
        safety_notes: result.safety_notes,
        sources: result.sources,
        operator_note: "",
      });
      message.success(`检修记录已生成：${workOrder.work_order_id}`);
      onWorkOrderCreated?.(workOrder.work_order_id);
    } catch (nextError) {
      message.error(nextError instanceof Error ? nextError.message : "生成检修记录失败。");
    } finally {
      setCreatingWorkOrder(false);
    }
  }

  return (
    <Space direction="vertical" size={20} className="page-fill">
      <Card>
        <Space direction="vertical" size={16} className="page-fill">
          <div>
            <Title level={4}>生成检修建议</Title>
            <Text type="secondary">系统会先检索知识库，再让模型基于参考片段生成结构化回答。</Text>
          </div>

          <Form
            form={form}
            layout="vertical"
            initialValues={{ question: DEFAULT_QUESTION }}
            onFinish={(values) => void handleSubmit(values)}
          >
            <Form.Item
              name="question"
              label="故障问题"
              rules={[{ required: true, message: "请先输入故障问题。" }]}
            >
              <TextArea rows={5} placeholder="输入设备故障现象或检修问题" />
            </Form.Item>

            <Form.Item name="equipment_type" label="设备类型（可选）">
              <Input placeholder="例如：电源模块、控制柜、空压机" />
            </Form.Item>

            <Space>
              <Button type="primary" htmlType="submit" icon={<SendOutlined />} loading={loading}>
                生成检修建议
              </Button>
              <Button
                onClick={() => {
                  form.resetFields();
                  setResult(null);
                  setError("");
                }}
                disabled={loading}
              >
                重置
              </Button>
            </Space>
          </Form>
        </Space>
      </Card>

      {error ? <Alert type="error" showIcon message={error} /> : null}

      {result ? (
        <div className="repair-result-grid">
          <Space direction="vertical" size={16} className="page-fill">
            <Card>
              <Space wrap>
                <Button
                  type="primary"
                  loading={creatingWorkOrder}
                  onClick={() => void handleCreateWorkOrder()}
                >
                  生成检修记录
                </Button>
                <Text type="secondary">将当前问题、RAG 输出和 sources 沉淀为 WorkOrder。</Text>
              </Space>
            </Card>
            <ResultCard title="故障理解" items={[result.fault_understanding]} />
            <ResultCard title="可能原因" items={result.possible_causes} ordered />
            <ResultCard title="排查步骤" items={result.repair_steps} ordered />
            <ResultCard title="安全注意事项" items={result.safety_notes} />

            {result.answer ? (
              <Collapse
                items={[
                  {
                    key: "raw",
                    label: "查看原始模型回答",
                    children: <pre className="raw-answer">{result.answer}</pre>,
                  },
                ]}
              />
            ) : null}
          </Space>

          <Card
            className="source-card-wrap"
            title={
              <Space>
                <RobotOutlined />
                依据来源
              </Space>
            }
            extra={<Tag color="blue">{result.sources.length}</Tag>}
          >
            {result.sources.length === 0 ? (
              <Alert type="warning" showIcon message="没有检索到可追溯来源。" />
            ) : (
              <List
                itemLayout="vertical"
                dataSource={result.sources}
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
        </div>
      ) : (
        <Alert
          type="info"
          showIcon
          message="等待输入故障问题"
          description="建议先用 scripts/test_rag_chat.py 验证后端问答质量，再在这里进行交互演示。"
        />
      )}
    </Space>
  );
}

function ResultCard({ title, items, ordered = false }: { title: string; items: string[]; ordered?: boolean }) {
  const normalizedItems = items.filter(Boolean);
  const ListTag = ordered ? "ol" : "ul";

  return (
    <Card title={title}>
      {normalizedItems.length === 0 ? (
        <Text type="secondary">暂无结构化内容。</Text>
      ) : (
        <ListTag className="result-list">
          {normalizedItems.map((item, index) => (
            <li key={`${title}-${index}`}>
              <Paragraph>{item}</Paragraph>
            </li>
          ))}
        </ListTag>
      )}
    </Card>
  );
}
