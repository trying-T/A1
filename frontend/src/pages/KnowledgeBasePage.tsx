import {
  CloudUploadOutlined,
  DatabaseOutlined,
  FileDoneOutlined,
  FileTextOutlined,
  ReloadOutlined,
} from "@ant-design/icons";
import { Alert, Button, Card, Col, Row, Space, Statistic, Table, Tag, Typography, Upload } from "antd";
import type { ColumnsType } from "antd/es/table";
import type { UploadProps } from "antd";
import { useEffect, useState } from "react";

import {
  chunkDocument,
  getDocuments,
  indexDocument,
  parseDocument,
  uploadDocument,
} from "../api/documentApi";
import type { DocumentItem } from "../types/document";

const { Text, Title } = Typography;

type ActionState = {
  loading: boolean;
  targetId: string | null;
  type: "upload" | "parse" | "chunk" | "index" | null;
};

const statusMap: Record<string, { label: string; color: string }> = {
  uploaded: { label: "已上传", color: "gold" },
  parsed: { label: "已解析", color: "blue" },
  chunked: { label: "已切分", color: "green" },
  indexed: { label: "已入库", color: "purple" },
};

export default function KnowledgeBasePage() {
  const [documents, setDocuments] = useState<DocumentItem[]>([]);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [pageLoading, setPageLoading] = useState(true);
  const [feedback, setFeedback] = useState("正在加载文档列表...");
  const [error, setError] = useState("");
  const [actionState, setActionState] = useState<ActionState>({
    loading: false,
    targetId: null,
    type: null,
  });

  useEffect(() => {
    void refreshDocuments();
  }, []);

  async function refreshDocuments() {
    setPageLoading(true);
    setError("");
    try {
      const result = await getDocuments();
      setDocuments(result.items);
      setFeedback(result.items.length > 0 ? "文档列表已更新。" : "当前还没有已上传文档。");
    } catch (nextError) {
      setError(getErrorMessage(nextError));
    } finally {
      setPageLoading(false);
    }
  }

  const uploadProps: UploadProps = {
    maxCount: 1,
    accept: ".pdf,.txt,.md,.markdown",
    beforeUpload: (file) => {
      setSelectedFile(file);
      setError("");
      return false;
    },
    onRemove: () => {
      setSelectedFile(null);
    },
  };

  async function handleUpload() {
    if (!selectedFile) {
      setError("请先选择一个 PDF、TXT 或 Markdown 文件。");
      return;
    }

    setActionState({ loading: true, targetId: null, type: "upload" });
    setError("");
    try {
      const result = await uploadDocument(selectedFile);
      setFeedback(result.message);
      setSelectedFile(null);
      await refreshDocuments();
    } catch (nextError) {
      setError(getErrorMessage(nextError));
    } finally {
      setActionState({ loading: false, targetId: null, type: null });
    }
  }

  async function runDocumentAction(
    documentId: string,
    type: ActionState["type"],
    action: () => Promise<{ message: string; chunk_count?: number | null }>,
  ) {
    setActionState({ loading: true, targetId: documentId, type });
    setError("");
    try {
      const result = await action();
      const suffix = result.chunk_count ? ` 共处理 ${result.chunk_count} 个片段。` : "";
      setFeedback(`${result.message}${suffix}`);
      await refreshDocuments();
    } catch (nextError) {
      setError(getErrorMessage(nextError));
    } finally {
      setActionState({ loading: false, targetId: null, type: null });
    }
  }

  const indexedCount = documents.filter((item) => item.status === "indexed").length;
  const chunkedCount = documents.filter((item) => item.status === "chunked").length;

  const columns: ColumnsType<DocumentItem> = [
    {
      title: "文件",
      dataIndex: "filename",
      render: (_, item) => (
        <Space direction="vertical" size={0}>
          <Text strong>{item.filename}</Text>
          <Text type="secondary">{item.document_id}</Text>
        </Space>
      ),
    },
    {
      title: "类型",
      dataIndex: "file_type",
      width: 110,
      render: (value: string) => <Tag>{value}</Tag>,
    },
    {
      title: "状态",
      dataIndex: "status",
      width: 120,
      render: (value: string) => {
        const status = statusMap[value] ?? { label: value, color: "default" };
        return <Tag color={status.color}>{status.label}</Tag>;
      },
    },
    {
      title: "上传时间",
      dataIndex: "upload_time",
      width: 190,
      render: (value: string) => formatDate(value),
    },
    {
      title: "操作",
      width: 240,
      render: (_, item) => {
        const isBusy = actionState.loading && actionState.targetId === item.document_id;
        return (
          <Space wrap>
            <Button
              size="small"
              loading={isBusy && actionState.type === "parse"}
              disabled={actionState.loading}
              onClick={() => void runDocumentAction(item.document_id, "parse", () => parseDocument(item.document_id))}
            >
              解析
            </Button>
            <Button
              size="small"
              loading={isBusy && actionState.type === "chunk"}
              disabled={actionState.loading || item.status === "uploaded"}
              onClick={() => void runDocumentAction(item.document_id, "chunk", () => chunkDocument(item.document_id))}
            >
              切分
            </Button>
            <Button
              size="small"
              type="primary"
              loading={isBusy && actionState.type === "index"}
              disabled={actionState.loading || item.status === "uploaded" || item.status === "parsed"}
              onClick={() => void runDocumentAction(item.document_id, "index", () => indexDocument(item.document_id))}
            >
              入库
            </Button>
          </Space>
        );
      },
    },
  ];

  return (
    <Space direction="vertical" size={20} className="page-fill">
      <Row gutter={[16, 16]}>
        <Col xs={24} md={8}>
          <Card>
            <Statistic title="文档总数" value={documents.length} prefix={<FileTextOutlined />} />
          </Card>
        </Col>
        <Col xs={24} md={8}>
          <Card>
            <Statistic title="已切分" value={chunkedCount} prefix={<FileDoneOutlined />} />
          </Card>
        </Col>
        <Col xs={24} md={8}>
          <Card>
            <Statistic title="已入库" value={indexedCount} prefix={<DatabaseOutlined />} />
          </Card>
        </Col>
      </Row>

      <Card>
        <Row gutter={[24, 16]} align="middle">
          <Col xs={24} lg={9}>
            <Title level={4}>上传检修资料</Title>
            <Text type="secondary">
              文件保存到 <Text code>data/uploads</Text>，初始状态为 <Text code>uploaded</Text>。
            </Text>
          </Col>
          <Col xs={24} lg={15}>
            <Space wrap align="start">
              <Upload {...uploadProps}>
                <Button icon={<CloudUploadOutlined />}>选择文档</Button>
              </Upload>
              <Button
                type="primary"
                loading={actionState.loading && actionState.type === "upload"}
                disabled={actionState.loading}
                onClick={() => void handleUpload()}
              >
                上传文档
              </Button>
            </Space>
          </Col>
        </Row>
      </Card>

      {error ? <Alert type="error" showIcon message={error} /> : <Alert type="success" showIcon message={feedback} />}

      <Card
        title="文档处理状态"
        extra={
          <Button icon={<ReloadOutlined />} onClick={() => void refreshDocuments()}>
            刷新
          </Button>
        }
      >
        <Table
          rowKey="document_id"
          loading={pageLoading}
          columns={columns}
          dataSource={documents}
          pagination={false}
          scroll={{ x: 860 }}
        />
      </Card>
    </Space>
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
