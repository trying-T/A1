import {
  DatabaseOutlined,
  ExperimentOutlined,
  FileProtectOutlined,
  RobotOutlined,
  SafetyCertificateOutlined,
} from "@ant-design/icons";
import { Badge, Layout, Menu, Space, Typography } from "antd";
import type { MenuProps } from "antd";
import { ReactNode } from "react";

type ActivePage = "knowledge" | "repair" | "workorders";

const { Header, Sider, Content } = Layout;
const { Text, Title } = Typography;

const menuItems: MenuProps["items"] = [
  {
    key: "knowledge-group",
    label: "知识中台",
    type: "group",
    children: [
      {
        key: "knowledge",
        icon: <DatabaseOutlined />,
        label: "知识库管理",
      },
    ],
  },
  {
    key: "repair-group",
    label: "智能检修",
    type: "group",
    children: [
      {
        key: "repair",
        icon: <RobotOutlined />,
        label: "检修问答",
      },
      {
        key: "workorders",
        icon: <FileProtectOutlined />,
        label: "检修记录",
      },
    ],
  },
];

const pageMeta: Record<ActivePage, { title: string; subtitle: string; icon: ReactNode }> = {
  knowledge: {
    title: "知识库管理",
    subtitle: "上传、解析、切分、向量入库，维护 RAG 检索前置数据。",
    icon: <ExperimentOutlined />,
  },
  repair: {
    title: "检修问答",
    subtitle: "基于知识片段生成检修建议，并保留 sources 便于人工复核。",
    icon: <SafetyCertificateOutlined />,
  },
  workorders: {
    title: "检修记录",
    subtitle: "沉淀 RAG 检修建议，形成可追溯的作业记录。",
    icon: <FileProtectOutlined />,
  },
};

export default function BasicLayout({
  activePage,
  onPageChange,
  children,
}: {
  activePage: ActivePage;
  onPageChange: (page: ActivePage) => void;
  children: ReactNode;
}) {
  const current = pageMeta[activePage];

  return (
    <Layout className="app-layout">
      <Sider className="app-sider" width={248} breakpoint="lg" collapsedWidth={0}>
        <div className="brand">
          <div className="brand-logo">A1</div>
          <div>
            <Text className="brand-title">Repair RAG</Text>
            <Text className="brand-subtitle">设备检修知识系统</Text>
          </div>
        </div>

        <Menu
          className="app-menu"
          mode="inline"
          selectedKeys={[activePage]}
          items={menuItems}
          onClick={({ key }) => onPageChange(key as ActivePage)}
        />

        <div className="sider-footer">
          <Text type="secondary">当前阶段</Text>
          <Text strong>RAG MVP</Text>
          <Text type="secondary">不做 Agent，优先保证链路可靠。</Text>
        </div>
      </Sider>

      <Layout>
        <Header className="app-header">
          <div className="page-title-wrap">
            <div className="page-icon">{current.icon}</div>
            <div>
              <Text type="secondary">首页 / {current.title}</Text>
              <Title level={3}>{current.title}</Title>
              <Text type="secondary">{current.subtitle}</Text>
            </div>
          </div>

          <Space className="header-actions">
            <Badge status="processing" text="本地开发环境" />
          </Space>
        </Header>

        <Content className="app-content">{children}</Content>
      </Layout>
    </Layout>
  );
}
