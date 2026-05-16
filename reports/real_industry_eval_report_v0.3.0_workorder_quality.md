# 真实工业 RAG 评测报告 v0.3.0 - WorkOrder 推荐质量治理

- generated_at: `2026-05-16 13:49:11`
- source_report: `data/demo/real_industry_eval_report.md`
- question_count: `24`
- 本报告基于 v0.3.0 第一阶段代码重新运行 24 题真实工业 RAG 评测，重点观察 WorkOrder 推荐质量。

## 汇总统计

- answer overall_passed 数量: `23/24`
- repair 触发次数: `11`
- safety guard 触发次数: `20`
- recommend_workorder=True 次数: `13`
- ready_to_create=True 次数: `13`
- ready_to_create=False 但 recommend_workorder=True 次数: `0`

> created_in_eval 指评测脚本是否通过 /workorders/create 另行创建了工单，不等于 RAG 推荐自动落库。

## 按题型分布

| type | total | recommend_workorder=True | ready_to_create=True | recommend=True 且 ready=False |
| --- | ---: | ---: | ---: | ---: |
| `smoke` | `6` | `1` | `1` | `0` |
| `parameter` | `6` | `0` | `0` | `0` |
| `procedure_fault` | `6` | `6` | `6` | `0` |
| `safety_boundary` | `6` | `6` | `6` | `0` |

## missing_fields 出现频次

- 无 missing_fields

## 重点题检查

| question_id | type | should_create_workorder | recommend_workorder | ready_to_create | missing_fields | reason |
| --- | --- | ---: | ---: | ---: | --- | --- |
| `param-001` | `parameter` | `False` | `False` | `False` | `` | `no_workorder_intent_detected` |
| `param-003` | `parameter` | `False` | `False` | `False` | `` | `no_workorder_intent_detected` |
| `fault-003` | `procedure_fault` | `True` | `True` | `True` | `` | `request_should_create_workorder, question_type_procedure_fault, explicit_execution_intent, safety_or_risk_related, fault_or_maintenance_intent` |
| `fault-006` | `procedure_fault` | `True` | `True` | `True` | `` | `request_should_create_workorder, question_type_procedure_fault, safety_or_risk_related, fault_or_maintenance_intent` |
| `safety-002` | `safety_boundary` | `True` | `True` | `True` | `` | `request_should_create_workorder, question_type_safety_boundary, explicit_execution_intent, safety_or_risk_related, fault_or_maintenance_intent` |
| `safety-003` | `safety_boundary` | `True` | `True` | `True` | `` | `request_should_create_workorder, question_type_safety_boundary, explicit_execution_intent, safety_or_risk_related` |

## 逐题诊断

### 01. `smoke-001` [smoke]

- question_id: `smoke-001`
- type: `smoke`
- answer_overall_passed: `True`
- score: `6/6`
- should_create_workorder: `False`
- recommend_workorder: `False`
- ready_to_create: `False`
- payload_preview.fault_symptom: 摩托车发动机火花塞应该如何检查和安装？请给出关键间隙和拧紧要求。
- payload_preview.inspection_steps: `1. 检查火花塞：目视检查火花塞螺纹及中心电极处，若有损坏或变形，则应更换火花塞。, 2. 测量间隙：用塞尺测量火花塞间隙a，标准值为0.7～0.9 mm，超出范围须更换火花塞。, 3. 安装火花塞前：确保火花塞孔及其周围没有灰尘，避免异物掉入气缸。, 4. 安装火花塞：将火花塞放入气缸头，套上火花塞专用套筒，顺时针转动3圈预紧，然后再转动1/4圈，或使用定扭扳手将其拧紧至20±2 N·m。, 5. 连接高压帽：用尖嘴钳将高压帽套进火花塞并用力往下压紧。`
- payload_preview.repair_steps: `1. 检查火花塞：目视检查火花塞螺纹及中心电极处，若有损坏或变形，则应更换火花塞。, 2. 测量间隙：用塞尺测量火花塞间隙a，标准值为0.7～0.9 mm，超出范围须更换火花塞。, 3. 安装火花塞前：确保火花塞孔及其周围没有灰尘，避免异物掉入气缸。, 4. 安装火花塞：将火花塞放入气缸头，套上火花塞专用套筒，顺时针转动3圈预紧，然后再转动1/4圈，或使用定扭扳手将其拧紧至20±2 N·m。, 5. 连接高压帽：用尖嘴钳将高压帽套进火花塞并用力往下压紧。`
- payload_preview.key_parameters: `0.7, 0.9, 20, N·m`
- payload_preview.safety_actions: ``
- payload_preview.source_chunk_ids: `chk-21541424d16a, chk-b91af999fdd1, chk-4d7f935536ae, chk-dfb84876691d, chk-ab08fbdb930b`
- payload_preview.missing_fields: ``
- created_in_eval: `False`
- 未 ready_to_create 原因: reason=no_workorder_intent_detected

work_order_recommendation raw:

```json
{
  "should_create_workorder": false,
  "recommend_workorder": false,
  "ready_to_create": false,
  "reason": "no_workorder_intent_detected",
  "explicit_execution_intent": false,
  "payload_preview": {
    "equipment_type": null,
    "fault_symptom": "摩托车发动机火花塞应该如何检查和安装？请给出关键间隙和拧紧要求。",
    "fault_understanding": "用户询问摩托车发动机火花塞的检查方法和安装步骤，包括关键间隙标准和拧紧力矩要求。",
    "possible_causes": [
      "无，用户询问标准操作流程。"
    ],
    "repair_steps": [
      "1. 检查火花塞：目视检查火花塞螺纹及中心电极处，若有损坏或变形，则应更换火花塞。",
      "2. 测量间隙：用塞尺测量火花塞间隙a，标准值为0.7～0.9 mm，超出范围须更换火花塞。",
      "3. 安装火花塞前：确保火花塞孔及其周围没有灰尘，避免异物掉入气缸。",
      "4. 安装火花塞：将火花塞放入气缸头，套上火花塞专用套筒，顺时针转动3圈预紧，然后再转动1/4圈，或使用定扭扳手将其拧紧至20±2 N·m。",
      "5. 连接高压帽：用尖嘴钳将高压帽套进火花塞并用力往下压紧。"
    ],
    "inspection_steps": [
      "1. 检查火花塞：目视检查火花塞螺纹及中心电极处，若有损坏或变形，则应更换火花塞。",
      "2. 测量间隙：用塞尺测量火花塞间隙a，标准值为0.7～0.9 mm，超出范围须更换火花塞。",
      "3. 安装火花塞前：确保火花塞孔及其周围没有灰尘，避免异物掉入气缸。",
      "4. 安装火花塞：将火花塞放入气缸头，套上火花塞专用套筒，顺时针转动3圈预紧，然后再转动1/4圈，或使用定扭扳手将其拧紧至20±2 N·m。",
      "5. 连接高压帽：用尖嘴钳将高压帽套进火花塞并用力往下压紧。"
    ],
    "key_parameters": [
      "0.7",
      "0.9",
      "20",
      "N·m"
    ],
    "safety_notes": [
      "确保发动机处于熄火冷却状态，避免烫伤。",
      "安装火花塞时使用专用套筒，避免损坏火花塞或气缸头螺纹。",
      "拧紧力矩不可过大，以免损坏螺纹；也不可过小，以免漏气或松动。",
      "拆卸火花塞之前要确保火花塞孔及其周围没有灰尘，以免异物掉入气缸。"
    ],
    "safety_actions": [],
    "source_chunk_ids": [
      "chk-21541424d16a",
      "chk-b91af999fdd1",
      "chk-4d7f935536ae",
      "chk-dfb84876691d",
      "chk-ab08fbdb930b"
    ],
    "missing_fields": [],
    "sources": [
      {
        "chunk_id": "chk-21541424d16a",
        "document_id": "doc-5a5e4729",
        "document_title": "摩托车发动机维修手册.pdf",
        "filename": "摩托车发动机维修手册.pdf",
        "chunk_index": 2,
        "score": 0.798056,
        "metadata": {
          "filename": "摩托车发动机维修手册.pdf",
          "file_type": "pdf",
          "chunk_size": 700,
          "overlap": 100,
          "start_offset": 1200,
          "end_offset": 1900,
          "document_id": "doc-5a5e4729",
          "chunk_id": "chk-21541424d16a",
          "chunk_index": 2,
          "source_type": "manual"
        }
      },
      {
        "chunk_id": "chk-b91af999fdd1",
        "document_id": "doc-5a5e4729",
        "document_title": "摩托车发动机维修手册.pdf",
        "filename": "摩托车发动机维修手册.pdf",
        "chunk_index": 1,
        "score": 0.714229,
        "metadata": {
          "filename": "摩托车发动机维修手册.pdf",
          "file_type": "pdf",
          "chunk_size": 700,
          "overlap": 100,
          "start_offset": 600,
          "end_offset": 1300,
          "document_id": "doc-5a5e4729",
          "chunk_id": "chk-b91af999fdd1",
          "chunk_index": 1,
          "source_type": "manual"
        }
      },
      {
        "chunk_id": "chk-4d7f935536ae",
        "document_id": "doc-5a5e4729",
        "document_title": "摩托车发动机维修手册.pdf",
        "filename": "摩托车发动机维修手册.pdf",
        "chunk_index": 13,
        "score": 0.697461,
        "metadata": {
          "filename": "摩托车发动机维修手册.pdf",
          "file_type": "pdf",
          "chunk_size": 700,
          "overlap": 100,
          "start_offset": 7800,
          "end_offset": 8500,
          "document_id": "doc-5a5e4729",
          "chunk_id": "chk-4d7f935536ae",
          "chunk_index": 13,
          "source_type": "manual"
        }
      },
      {
        "chunk_id": "chk-dfb84876691d",
        "document_id": "doc-5a5e4729",
        "document_title": "摩托车发动机维修手册.pdf",
        "filename": "摩托车发动机维修手册.pdf",
        "chunk_index": 5,
        "score": 0.692629,
        "metadata": {
          "filename": "摩托车发动机维修手册.pdf",
          "file_type": "pdf",
          "chunk_size": 700,
          "overlap": 100,
          "start_offset": 3000,
          "end_offset": 3700,
          "document_id": "doc-5a5e4729",
          "chunk_id": "chk-dfb84876691d",
          "chunk_index": 5,
          "source_type": "manual"
        }
      },
      {
        "chunk_id": "chk-ab08fbdb930b",
        "document_id": "doc-5a5e4729",
        "document_title": "摩托车发动机维修手册.pdf",
        "filename": "摩托车发动机维修手册.pdf",
        "chunk_index": 9,
        "score": 0.688442,
        "metadata": {
          "filename": "摩托车发动机维修手册.pdf",
          "file_type": "pdf",
          "chunk_size": 700,
          "overlap": 100,
          "start_offset": 5400,
          "end_offset": 6100,
          "document_id": "doc-5a5e4729",
          "chunk_id": "chk-ab08fbdb930b",
          "chunk_index": 9,
          "source_type": "manual"
        }
      }
    ],
    "operator_note": "Generated from RAG work_order_recommendation."
  },
  "work_order_quality_check": {
    "passed": true,
    "errors": [],
    "ready_to_create": false,
    "recommend_workorder": false,
    "missing_fields": []
  }
}
```

### 02. `smoke-002` [smoke]

- question_id: `smoke-002`
- type: `smoke`
- answer_overall_passed: `True`
- score: `6/6`
- should_create_workorder: `False`
- recommend_workorder: `False`
- ready_to_create: `False`
- payload_preview.fault_symptom: AH3 机器人维护手册主要面向哪些维护内容？日常维护时应关注哪些安全提示？
- payload_preview.inspection_steps: ``
- payload_preview.repair_steps: ``
- payload_preview.key_parameters: `AH3`
- payload_preview.safety_actions: `停止设备或相关运动。, 切断电源、气源或其他能量源。, 确认安全栅、联锁门、急停或示教器等安全装置状态。, 不允许在风险未隔离前继续操作或恢复运行。, 禁止在资料依据不足时执行高风险检修步骤。, 由受训人员或具备电气/机械维护资格的人员处理。`
- payload_preview.source_chunk_ids: `chk-34e24f914071, chk-584614b08045, chk-f836f9d469f8, chk-7d795b762e99, chk-a9523db152cf`
- payload_preview.missing_fields: ``
- created_in_eval: `False`
- 未 ready_to_create 原因: reason=no_workorder_intent_detected

work_order_recommendation raw:

```json
{
  "should_create_workorder": false,
  "recommend_workorder": false,
  "ready_to_create": false,
  "reason": "no_workorder_intent_detected",
  "explicit_execution_intent": false,
  "payload_preview": {
    "equipment_type": null,
    "fault_symptom": "AH3 机器人维护手册主要面向哪些维护内容？日常维护时应关注哪些安全提示？",
    "fault_understanding": "用户询问AH3机器人维护手册覆盖的维护内容以及日常维护时应关注的安全提示。根据资料，手册主要涉及日常维护保养、安全检查、机械及电气零部件保养，并包含安全停机注意事项、安全标识等安全提示。",
    "possible_causes": [],
    "repair_steps": [],
    "inspection_steps": [],
    "key_parameters": [
      "AH3"
    ],
    "safety_notes": [
      "设备长时间断电再度使用时易出现电池异常，因此长时间停用前应使机器人处于原点位置。",
      "降低机器人速度后再下伺服，下伺服后再关闭电源。",
      "回收设备相关物料，确保设备恢复至可安全重启状态。",
      "设立防护装置，标明设备当前状态，防止他人误操作。",
      "机器人再次启动前建议间隔约1分钟，勿关闭电源后立即重启。",
      "机器人再次启动前需检查Emergency stop（急停）按钮是否松开，避免机器人不能上伺服。",
      "注意机器人主体上的警告标签：三角高压警示标识、接地标识、残余电压防护标识、禁止拆解标识。",
      "日常维护时需执行接通电源前的检测项目（如气管、紧固螺钉等），并按照手册要求的安全操作进行。",
      "维护后需测试机器人及功能完整性。",
      "停止设备或相关运动。",
      "切断电源、气源或其他能量源。",
      "确认安全栅、联锁门、急停或示教器等安全装置状态。",
      "不允许在风险未隔离前继续操作或恢复运行。",
      "禁止在资料依据不足时执行高风险检修步骤。",
      "由受训人员或具备电气/机械维护资格的人员处理。",
      "本文图标将明确说明执行此手册中描述的工作时，可能出现的所有危险、警告、注意和",
      "机器人主体上粘贴有下述警告标签",
      "为了安全地操作、维护机器人系统，请务必遵守警告标签上记载的注意与警告内容",
      "表 1-1 警告标识表",
      "禁止拆解，避免发"
    ],
    "safety_actions": [
      "停止设备或相关运动。",
      "切断电源、气源或其他能量源。",
      "确认安全栅、联锁门、急停或示教器等安全装置状态。",
      "不允许在风险未隔离前继续操作或恢复运行。",
      "禁止在资料依据不足时执行高风险检修步骤。",
      "由受训人员或具备电气/机械维护资格的人员处理。"
    ],
    "source_chunk_ids": [
      "chk-34e24f914071",
      "chk-584614b08045",
      "chk-f836f9d469f8",
      "chk-7d795b762e99",
      "chk-a9523db152cf"
    ],
    "missing_fields": [],
    "sources": [
      {
        "chunk_id": "chk-34e24f914071",
        "document_id": "doc-7148b79c",
        "document_title": "AH3 机器人维护手册 V1.1.5.pdf",
        "filename": "AH3 机器人维护手册 V1.1.5.pdf",
        "chunk_index": 0,
        "score": 0.816121,
        "metadata": {
          "filename": "AH3 机器人维护手册 V1.1.5.pdf",
          "file_type": "pdf",
          "chunk_size": 700,
          "overlap": 100,
          "start_offset": 0,
          "end_offset": 700,
          "document_id": "doc-7148b79c",
          "chunk_id": "chk-34e24f914071",
          "chunk_index": 0,
          "source_type": "manual"
        }
      },
      {
        "chunk_id": "chk-584614b08045",
        "document_id": "doc-7148b79c",
        "document_title": "AH3 机器人维护手册 V1.1.5.pdf",
        "filename": "AH3 机器人维护手册 V1.1.5.pdf",
        "chunk_index": 21,
        "score": 0.746096,
        "metadata": {
          "filename": "AH3 机器人维护手册 V1.1.5.pdf",
          "file_type": "pdf",
          "chunk_size": 700,
          "overlap": 100,
          "start_offset": 12600,
          "end_offset": 13300,
          "document_id": "doc-7148b79c",
          "chunk_id": "chk-584614b08045",
          "chunk_index": 21,
          "source_type": "manual"
        }
      },
      {
        "chunk_id": "chk-f836f9d469f8",
        "document_id": "doc-7148b79c",
        "document_title": "AH3 机器人维护手册 V1.1.5.pdf",
        "filename": "AH3 机器人维护手册 V1.1.5.pdf",
        "chunk_index": 15,
        "score": 0.73096,
        "metadata": {
          "filename": "AH3 机器人维护手册 V1.1.5.pdf",
          "file_type": "pdf",
          "chunk_size": 700,
          "overlap": 100,
          "start_offset": 9000,
          "end_offset": 9700,
          "document_id": "doc-7148b79c",
          "chunk_id": "chk-f836f9d469f8",
          "chunk_index": 15,
          "source_type": "manual"
        }
      },
      {
        "chunk_id": "chk-7d795b762e99",
        "document_id": "doc-7148b79c",
        "document_title": "AH3 机器人维护手册 V1.1.5.pdf",
        "filename": "AH3 机器人维护手册 V1.1.5.pdf",
        "chunk_index": 4,
        "score": 0.72899,
        "metadata": {
          "filename": "AH3 机器人维护手册 V1.1.5.pdf",
          "file_type": "pdf",
          "chunk_size": 700,
          "overlap": 100,
          "start_offset": 2400,
          "end_offset": 3100,
          "document_id": "doc-7148b79c",
          "chunk_id": "chk-7d795b762e99",
          "chunk_index": 4,
          "source_type": "manual"
        }
      },
      {
        "chunk_id": "chk-a9523db152cf",
        "document_id": "doc-7148b79c",
        "document_title": "AH3 机器人维护手册 V1.1.5.pdf",
        "filename": "AH3 机器人维护手册 V1.1.5.pdf",
        "chunk_index": 22,
        "score": 0.726166,
        "metadata": {
          "filename": "AH3 机器人维护手册 V1.1.5.pdf",
          "file_type": "pdf",
          "chunk_size": 700,
          "overlap": 100,
          "start_offset": 13200,
          "end_offset": 13900,
          "document_id": "doc-7148b79c",
          "chunk_id": "chk-a9523db152cf",
          "chunk_index": 22,
          "source_type": "manual"
        }
      }
    ],
    "operator_note": "Generated from RAG work_order_recommendation."
  },
  "work_order_quality_check": {
    "passed": true,
    "errors": [],
    "ready_to_create": false,
    "recommend_workorder": false,
    "missing_fields": []
  }
}
```

### 03. `smoke-003` [smoke]

- question_id: `smoke-003`
- type: `smoke`
- answer_overall_passed: `False`
- score: `5/6`
- should_create_workorder: `False`
- recommend_workorder: `False`
- ready_to_create: `False`
- payload_preview.fault_symptom: bfp-a3570l 安全手册中的剩余风险地图和剩余风险一览表是用来做什么的？
- payload_preview.inspection_steps: `1. 查阅BFP-A3570-L安全手册中的剩余风险地图，找到与当前操作（如开箱、搬运、示教自动运行、维护点检）对应的部位和风险编号。, 2. 根据风险编号，在剩余风险一览表中找到对应条目，识别该风险的危害内容、危害程度（危险/警告/注意）以及推荐的保护措施。, 3. 按照一览表中列出的保护措施实施必要的安全对策（例如按规定方法搬运、使用合格资格人员操作等），并参照对应的使用说明书进一步操作。`
- payload_preview.repair_steps: `1. 查阅BFP-A3570-L安全手册中的剩余风险地图，找到与当前操作（如开箱、搬运、示教自动运行、维护点检）对应的部位和风险编号。, 2. 根据风险编号，在剩余风险一览表中找到对应条目，识别该风险的危害内容、危害程度（危险/警告/注意）以及推荐的保护措施。, 3. 按照一览表中列出的保护措施实施必要的安全对策（例如按规定方法搬运、使用合格资格人员操作等），并参照对应的使用说明书进一步操作。`
- payload_preview.key_parameters: ``
- payload_preview.safety_actions: `停止设备或相关运动。, 切断电源、气源或其他能量源。, 确认安全栅、联锁门、急停或示教器等安全装置状态。, 资料片段中未检索到明确的立即行动要求。, 不允许在风险未隔离前继续操作或恢复运行。, 禁止在资料依据不足时执行高风险检修步骤。, 资料片段中未检索到明确的禁止操作内容。, 由受训人员或具备电气/机械维护资格的人员处理。, 资料片段中提及搬运机器人本体需由持有劳动安全卫生法规定的起吊机或叉车驾驶资格的人员操作。`
- payload_preview.source_chunk_ids: `chk-6d506dc17126, chk-5e0af5c054da, chk-27c9c85ace60, chk-2fa410c18c12, chk-f836f9d469f8`
- payload_preview.missing_fields: ``
- created_in_eval: `False`
- 未 ready_to_create 原因: reason=no_workorder_intent_detected

work_order_recommendation raw:

```json
{
  "should_create_workorder": false,
  "recommend_workorder": false,
  "ready_to_create": false,
  "reason": "no_workorder_intent_detected",
  "explicit_execution_intent": false,
  "payload_preview": {
    "equipment_type": null,
    "fault_symptom": "bfp-a3570l 安全手册中的剩余风险地图和剩余风险一览表是用来做什么的？",
    "fault_understanding": "用户询问三菱电机工业机器人安全手册BFP-A3570-L中剩余风险地图和剩余风险一览表的功能。根据手册描述，剩余风险地图以图示方式标出机器人各个部位对应的剩余风险编号及危险等级，并与剩余风险一览表关联；剩余风险一览表则详细列出每个编号对应的运用阶段、作业内容、危害程度、具体危害描述以及机械用户应实施的保护措施。两者共同用于指导机械用户识别和应对未实施保护措施时仍残留的风险。",
    "possible_causes": [
      "手册说明：剩余风险地图中的编号对应剩余风险一览表中的保护措施编号，帮助用户定位并理解各部位风险。",
      "剩余风险一览表提供了危害内容、危害程度及机械用户应实施的保护措施，是用户制定安全对策的依据。"
    ],
    "repair_steps": [
      "1. 查阅BFP-A3570-L安全手册中的剩余风险地图，找到与当前操作（如开箱、搬运、示教自动运行、维护点检）对应的部位和风险编号。",
      "2. 根据风险编号，在剩余风险一览表中找到对应条目，识别该风险的危害内容、危害程度（危险/警告/注意）以及推荐的保护措施。",
      "3. 按照一览表中列出的保护措施实施必要的安全对策（例如按规定方法搬运、使用合格资格人员操作等），并参照对应的使用说明书进一步操作。"
    ],
    "inspection_steps": [
      "1. 查阅BFP-A3570-L安全手册中的剩余风险地图，找到与当前操作（如开箱、搬运、示教自动运行、维护点检）对应的部位和风险编号。",
      "2. 根据风险编号，在剩余风险一览表中找到对应条目，识别该风险的危害内容、危害程度（危险/警告/注意）以及推荐的保护措施。",
      "3. 按照一览表中列出的保护措施实施必要的安全对策（例如按规定方法搬运、使用合格资格人员操作等），并参照对应的使用说明书进一步操作。"
    ],
    "key_parameters": [],
    "safety_notes": [
      "务必理解本资料仅为使用说明书的参考资料，不可仅凭本资料直接使用产品。",
      "剩余风险地图和一览表仅列出已知的剩余风险，实际使用中仍需结合完整使用说明书进行风险评估。",
      "搬运、起吊等操作需由具备相应资格的人员执行，并遵守劳动安全卫生法规。",
      "停止设备或相关运动。",
      "切断电源、气源或其他能量源。",
      "确认安全栅、联锁门、急停或示教器等安全装置状态。",
      "不允许在风险未隔离前继续操作或恢复运行。",
      "禁止在资料依据不足时执行高风险检修步骤。",
      "由受训人员或具备电气/机械维护资格的人员处理。",
      "危险",
      "警告",
      "部位 B No.2、3、6、7 危险",
      "而言危险且严酷的场所也可长时间地持续工作",
      "特有危险",
      "资料片段中未检索到明确的立即行动要求。",
      "资料片段中未检索到明确的禁止操作内容。",
      "资料片段中提及搬运机器人本体需由持有劳动安全卫生法规定的起吊机或叉车驾驶资格的人员操作。",
      "剩余风险地图：图示编号对应部位及危险等级。",
      "剩余风险一览表：编号对应的运用阶段、作业内容、危害程度、危害内容及保护措施。",
      "危险：未实施保护措施时可能发生人员伤亡或重伤。",
      "警告：未实施保护措施时可能发生人员轻伤。",
      "注意：未实施保护措施时可能发生轻伤事故。"
    ],
    "safety_actions": [
      "停止设备或相关运动。",
      "切断电源、气源或其他能量源。",
      "确认安全栅、联锁门、急停或示教器等安全装置状态。",
      "资料片段中未检索到明确的立即行动要求。",
      "不允许在风险未隔离前继续操作或恢复运行。",
      "禁止在资料依据不足时执行高风险检修步骤。",
      "资料片段中未检索到明确的禁止操作内容。",
      "由受训人员或具备电气/机械维护资格的人员处理。",
      "资料片段中提及搬运机器人本体需由持有劳动安全卫生法规定的起吊机或叉车驾驶资格的人员操作。"
    ],
    "source_chunk_ids": [
      "chk-6d506dc17126",
      "chk-5e0af5c054da",
      "chk-27c9c85ace60",
      "chk-2fa410c18c12",
      "chk-f836f9d469f8"
    ],
    "missing_fields": [],
    "sources": [
      {
        "chunk_id": "chk-6d506dc17126",
        "document_id": "doc-b64a3971",
        "document_title": "bfp-a3570l.pdf",
        "filename": "bfp-a3570l.pdf",
        "chunk_index": 0,
        "score": 0.692703,
        "metadata": {
          "filename": "bfp-a3570l.pdf",
          "file_type": "pdf",
          "chunk_size": 700,
          "overlap": 100,
          "start_offset": 0,
          "end_offset": 700,
          "document_id": "doc-b64a3971",
          "chunk_id": "chk-6d506dc17126",
          "chunk_index": 0,
          "source_type": "manual"
        }
      },
      {
        "chunk_id": "chk-5e0af5c054da",
        "document_id": "doc-b64a3971",
        "document_title": "bfp-a3570l.pdf",
        "filename": "bfp-a3570l.pdf",
        "chunk_index": 1,
        "score": 0.58272,
        "metadata": {
          "filename": "bfp-a3570l.pdf",
          "file_type": "pdf",
          "chunk_size": 700,
          "overlap": 100,
          "start_offset": 600,
          "end_offset": 1300,
          "document_id": "doc-b64a3971",
          "chunk_id": "chk-5e0af5c054da",
          "chunk_index": 1,
          "source_type": "manual"
        }
      },
      {
        "chunk_id": "chk-27c9c85ace60",
        "document_id": "doc-b64a3971",
        "document_title": "bfp-a3570l.pdf",
        "filename": "bfp-a3570l.pdf",
        "chunk_index": 18,
        "score": 0.571339,
        "metadata": {
          "filename": "bfp-a3570l.pdf",
          "file_type": "pdf",
          "chunk_size": 700,
          "overlap": 100,
          "start_offset": 10800,
          "end_offset": 11500,
          "document_id": "doc-b64a3971",
          "chunk_id": "chk-27c9c85ace60",
          "chunk_index": 18,
          "source_type": "manual"
        }
      },
      {
        "chunk_id": "chk-2fa410c18c12",
        "document_id": "doc-b9a5aa33",
        "document_title": "safety manual for fanuc educational cell.pdf",
        "filename": "safety manual for fanuc educational cell.pdf",
        "chunk_index": 7,
        "score": 0.567688,
        "metadata": {
          "filename": "safety manual for fanuc educational cell.pdf",
          "file_type": "pdf",
          "chunk_size": 700,
          "overlap": 100,
          "start_offset": 4200,
          "end_offset": 4900,
          "document_id": "doc-b9a5aa33",
          "chunk_id": "chk-2fa410c18c12",
          "chunk_index": 7,
          "source_type": "manual"
        }
      },
      {
        "chunk_id": "chk-f836f9d469f8",
        "document_id": "doc-7148b79c",
        "document_title": "AH3 机器人维护手册 V1.1.5.pdf",
        "filename": "AH3 机器人维护手册 V1.1.5.pdf",
        "chunk_index": 15,
        "score": 0.550905,
        "metadata": {
          "filename": "AH3 机器人维护手册 V1.1.5.pdf",
          "file_type": "pdf",
          "chunk_size": 700,
          "overlap": 100,
          "start_offset": 9000,
          "end_offset": 9700,
          "document_id": "doc-7148b79c",
          "chunk_id": "chk-f836f9d469f8",
          "chunk_index": 15,
          "source_type": "manual"
        }
      }
    ],
    "operator_note": "Generated from RAG work_order_recommendation."
  },
  "work_order_quality_check": {
    "passed": true,
    "errors": [],
    "ready_to_create": false,
    "recommend_workorder": false,
    "missing_fields": []
  }
}
```

### 04. `smoke-004` [smoke]

- question_id: `smoke-004`
- type: `smoke`
- answer_overall_passed: `True`
- score: `6/6`
- should_create_workorder: `False`
- recommend_workorder: `False`
- ready_to_create: `False`
- payload_preview.fault_symptom: FANUC educational cell 安全手册说明了哪些机器人安全使用注意事项？
- payload_preview.inspection_steps: `1. 使用前务必阅读并理解本安全手册的全部内容。, 2. 确认操作人员已接受适当培训，未受训人员不得进入安全栅（safety fence）内部。, 3. 在操作机器人时，安排一名熟悉机器人系统的人员站在操作面板旁观察，并随时准备按下紧急停止（Emergency stop）按钮。, 4. 更换部件时，务必联系当地FANUC代表并遵循正确程序，防止错误操作导致事故。, 5. 更换或重装组件时，注意防止异物进入系统内部。, 6. 检查控制器内单元或印刷电路板前，先关闭断路器（circuit breaker）以确保断电，避免触电。, 7. 遵守机器人安装所在地的法律法规及相关安全标准（如EN/ISO 10218-1、EN 60204-1等）。`
- payload_preview.repair_steps: `1. 使用前务必阅读并理解本安全手册的全部内容。, 2. 确认操作人员已接受适当培训，未受训人员不得进入安全栅（safety fence）内部。, 3. 在操作机器人时，安排一名熟悉机器人系统的人员站在操作面板旁观察，并随时准备按下紧急停止（Emergency stop）按钮。, 4. 更换部件时，务必联系当地FANUC代表并遵循正确程序，防止错误操作导致事故。, 5. 更换或重装组件时，注意防止异物进入系统内部。, 6. 检查控制器内单元或印刷电路板前，先关闭断路器（circuit breaker）以确保断电，避免触电。, 7. 遵守机器人安装所在地的法律法规及相关安全标准（如EN/ISO 10218-1、EN 60204-1等）。`
- payload_preview.key_parameters: `FANUC, safety, robot, emergency`
- payload_preview.safety_actions: `停止设备或相关运动。, 切断电源、气源或其他能量源。, 确认安全栅、联锁门、急停或示教器等安全装置状态。, 不允许在风险未隔离前继续操作或恢复运行。, 禁止在资料依据不足时执行高风险检修步骤。, 由受训人员或具备电气/机械维护资格的人员处理。`
- payload_preview.source_chunk_ids: `chk-c16663488d97, chk-5e0af5c054da, chk-9b93b9d6895c, chk-877bfd5c9b10, chk-6a6965a98897`
- payload_preview.missing_fields: ``
- created_in_eval: `False`
- 未 ready_to_create 原因: reason=no_workorder_intent_detected

work_order_recommendation raw:

```json
{
  "should_create_workorder": false,
  "recommend_workorder": false,
  "ready_to_create": false,
  "reason": "no_workorder_intent_detected",
  "explicit_execution_intent": false,
  "payload_preview": {
    "equipment_type": null,
    "fault_symptom": "FANUC educational cell 安全手册说明了哪些机器人安全使用注意事项？",
    "fault_understanding": "用户询问FANUC educational cell安全手册中说明了哪些机器人安全使用注意事项。根据手册片段，内容包括：安全培训要求、安全围栏内工作限制、紧急停止（Emergency stop）措施、部件更换规范、电气安全操作等。此外，手册特别强调使用FANUC robot前必须阅读本手册，并遵守相关标准（如EN/ISO 10218-1）。",
    "possible_causes": [
      "未经适当培训的人员在安全围栏内工作可能导致被机器人手臂挤压等严重伤害或死亡。",
      "未在操作过程中安排熟悉系统的人员观察并准备按下紧急停止（Emergency stop）按钮，可能无法及时应对危险。",
      "错误地更换部件或使用非正规程序可能导致机器人损坏或人员受伤。",
      "更换或重装组件时异物进入系统可能引发故障。",
      "在检查控制器时未关闭断路器（circuit breaker）可能导致触电。",
      "未阅读并理解安全手册，导致操作违反安全标准。"
    ],
    "repair_steps": [
      "1. 使用前务必阅读并理解本安全手册的全部内容。",
      "2. 确认操作人员已接受适当培训，未受训人员不得进入安全栅（safety fence）内部。",
      "3. 在操作机器人时，安排一名熟悉机器人系统的人员站在操作面板旁观察，并随时准备按下紧急停止（Emergency stop）按钮。",
      "4. 更换部件时，务必联系当地FANUC代表并遵循正确程序，防止错误操作导致事故。",
      "5. 更换或重装组件时，注意防止异物进入系统内部。",
      "6. 检查控制器内单元或印刷电路板前，先关闭断路器（circuit breaker）以确保断电，避免触电。",
      "7. 遵守机器人安装所在地的法律法规及相关安全标准（如EN/ISO 10218-1、EN 60204-1等）。"
    ],
    "inspection_steps": [
      "1. 使用前务必阅读并理解本安全手册的全部内容。",
      "2. 确认操作人员已接受适当培训，未受训人员不得进入安全栅（safety fence）内部。",
      "3. 在操作机器人时，安排一名熟悉机器人系统的人员站在操作面板旁观察，并随时准备按下紧急停止（Emergency stop）按钮。",
      "4. 更换部件时，务必联系当地FANUC代表并遵循正确程序，防止错误操作导致事故。",
      "5. 更换或重装组件时，注意防止异物进入系统内部。",
      "6. 检查控制器内单元或印刷电路板前，先关闭断路器（circuit breaker）以确保断电，避免触电。",
      "7. 遵守机器人安装所在地的法律法规及相关安全标准（如EN/ISO 10218-1、EN 60204-1等）。"
    ],
    "key_parameters": [
      "FANUC",
      "safety",
      "robot",
      "emergency"
    ],
    "safety_notes": [
      "警告（Warning）：用于表示可能导致死亡或严重伤害的危险情况。",
      "注意（Caution）：用于表示可能导致轻度或中度伤害的危险情况。",
      "在安全栅（safety fence）内工作前必须经过培训，否则可能因被夹住等危险导致严重伤害或死亡。",
      "紧急停止（Emergency stop）按钮应在任何危险出现时立即按下。",
      "电气检查时必须完全切断电源（关闭断路器），以防触电。",
      "更换部件若操作不当可能造成机器人损坏或人员伤害，建议由专业FANUC代表执行。",
      "停止设备或相关运动。",
      "切断电源、气源或其他能量源。",
      "确认安全栅、联锁门、急停或示教器等安全装置状态。",
      "不允许在风险未隔离前继续操作或恢复运行。",
      "禁止在资料依据不足时执行高风险检修步骤。",
      "由受训人员或具备电气/机械维护资格的人员处理。",
      "on safety with \"Warning\" or \"Caution\" according to its severit",
      "危险",
      "observe the work being performed. If any danger arises, the user should be ready to press the",
      "· 禁止未经允许转载本手册的部分或全部内容",
      "To ensure the safety of workers and prevent damage to the machine, this manual indicates each precaution",
      "在安全栅（safety fence）内工作前必须经过培训，否则可能因被机器人手臂夹住等危险导致严重伤害或死亡。",
      "Before using the FANUC robot, be sure to read this manual to understand the contents."
    ],
    "safety_actions": [
      "停止设备或相关运动。",
      "切断电源、气源或其他能量源。",
      "确认安全栅、联锁门、急停或示教器等安全装置状态。",
      "不允许在风险未隔离前继续操作或恢复运行。",
      "禁止在资料依据不足时执行高风险检修步骤。",
      "由受训人员或具备电气/机械维护资格的人员处理。"
    ],
    "source_chunk_ids": [
      "chk-c16663488d97",
      "chk-5e0af5c054da",
      "chk-9b93b9d6895c",
      "chk-877bfd5c9b10",
      "chk-6a6965a98897"
    ],
    "missing_fields": [],
    "sources": [
      {
        "chunk_id": "chk-c16663488d97",
        "document_id": "doc-b9a5aa33",
        "document_title": "safety manual for fanuc educational cell.pdf",
        "filename": "safety manual for fanuc educational cell.pdf",
        "chunk_index": 5,
        "score": 0.699092,
        "metadata": {
          "filename": "safety manual for fanuc educational cell.pdf",
          "file_type": "pdf",
          "chunk_size": 700,
          "overlap": 100,
          "start_offset": 3000,
          "end_offset": 3700,
          "document_id": "doc-b9a5aa33",
          "chunk_id": "chk-c16663488d97",
          "chunk_index": 5,
          "source_type": "manual"
        }
      },
      {
        "chunk_id": "chk-5e0af5c054da",
        "document_id": "doc-b64a3971",
        "document_title": "bfp-a3570l.pdf",
        "filename": "bfp-a3570l.pdf",
        "chunk_index": 1,
        "score": 0.683044,
        "metadata": {
          "filename": "bfp-a3570l.pdf",
          "file_type": "pdf",
          "chunk_size": 700,
          "overlap": 100,
          "start_offset": 600,
          "end_offset": 1300,
          "document_id": "doc-b64a3971",
          "chunk_id": "chk-5e0af5c054da",
          "chunk_index": 1,
          "source_type": "manual"
        }
      },
      {
        "chunk_id": "chk-9b93b9d6895c",
        "document_id": "doc-b9a5aa33",
        "document_title": "safety manual for fanuc educational cell.pdf",
        "filename": "safety manual for fanuc educational cell.pdf",
        "chunk_index": 27,
        "score": 0.672677,
        "metadata": {
          "filename": "safety manual for fanuc educational cell.pdf",
          "file_type": "pdf",
          "chunk_size": 700,
          "overlap": 100,
          "start_offset": 16200,
          "end_offset": 16900,
          "document_id": "doc-b9a5aa33",
          "chunk_id": "chk-9b93b9d6895c",
          "chunk_index": 27,
          "source_type": "manual"
        }
      },
      {
        "chunk_id": "chk-877bfd5c9b10",
        "document_id": "doc-b9a5aa33",
        "document_title": "safety manual for fanuc educational cell.pdf",
        "filename": "safety manual for fanuc educational cell.pdf",
        "chunk_index": 150,
        "score": 0.671748,
        "metadata": {
          "filename": "safety manual for fanuc educational cell.pdf",
          "file_type": "pdf",
          "chunk_size": 700,
          "overlap": 100,
          "start_offset": 90000,
          "end_offset": 90700,
          "document_id": "doc-b9a5aa33",
          "chunk_id": "chk-877bfd5c9b10",
          "chunk_index": 150,
          "source_type": "manual"
        }
      },
      {
        "chunk_id": "chk-6a6965a98897",
        "document_id": "doc-b64a3971",
        "document_title": "bfp-a3570l.pdf",
        "filename": "bfp-a3570l.pdf",
        "chunk_index": 19,
        "score": 0.665423,
        "metadata": {
          "filename": "bfp-a3570l.pdf",
          "file_type": "pdf",
          "chunk_size": 700,
          "overlap": 100,
          "start_offset": 11400,
          "end_offset": 12100,
          "document_id": "doc-b64a3971",
          "chunk_id": "chk-6a6965a98897",
          "chunk_index": 19,
          "source_type": "manual"
        }
      }
    ],
    "operator_note": "Generated from RAG work_order_recommendation."
  },
  "work_order_quality_check": {
    "passed": true,
    "errors": [],
    "ready_to_create": false,
    "recommend_workorder": false,
    "missing_fields": []
  }
}
```

### 05. `smoke-005` [smoke]

- question_id: `smoke-005`
- type: `smoke`
- answer_overall_passed: `True`
- score: `6/6`
- should_create_workorder: `False`
- recommend_workorder: `False`
- ready_to_create: `False`
- payload_preview.fault_symptom: CM2x-OM0230Q 气缸手册包含哪些主要章节？
- payload_preview.inspection_steps: ``
- payload_preview.repair_steps: ``
- payload_preview.key_parameters: ``
- payload_preview.safety_actions: ``
- payload_preview.source_chunk_ids: `chk-65d6cca0f77c, chk-144fe11aea33, chk-d185bce0f648, chk-44ce5ae9159a, chk-763a8cf76e61`
- payload_preview.missing_fields: ``
- created_in_eval: `False`
- 未 ready_to_create 原因: reason=no_workorder_intent_detected

work_order_recommendation raw:

```json
{
  "should_create_workorder": false,
  "recommend_workorder": false,
  "ready_to_create": false,
  "reason": "no_workorder_intent_detected",
  "explicit_execution_intent": false,
  "payload_preview": {
    "equipment_type": null,
    "fault_symptom": "CM2x-OM0230Q 气缸手册包含哪些主要章节？",
    "fault_understanding": "基于参考资料CM2x-OM0230Q.pdf的目录，用户询问该气缸手册包含的主要章节。知识库中提供了完整的目录信息。",
    "possible_causes": [],
    "repair_steps": [],
    "inspection_steps": [],
    "key_parameters": [],
    "safety_notes": [
      "手册包含安全注意事项章节，建议使用前详细阅读。"
    ],
    "safety_actions": [],
    "source_chunk_ids": [
      "chk-65d6cca0f77c",
      "chk-144fe11aea33",
      "chk-d185bce0f648",
      "chk-44ce5ae9159a",
      "chk-763a8cf76e61"
    ],
    "missing_fields": [],
    "sources": [
      {
        "chunk_id": "chk-65d6cca0f77c",
        "document_id": "doc-bc2d279f",
        "document_title": "CM2x-OM0230Q.pdf",
        "filename": "CM2x-OM0230Q.pdf",
        "chunk_index": 0,
        "score": 0.676752,
        "metadata": {
          "filename": "CM2x-OM0230Q.pdf",
          "file_type": "pdf",
          "chunk_size": 700,
          "overlap": 100,
          "start_offset": 0,
          "end_offset": 700,
          "document_id": "doc-bc2d279f",
          "chunk_id": "chk-65d6cca0f77c",
          "chunk_index": 0,
          "source_type": "manual"
        }
      },
      {
        "chunk_id": "chk-144fe11aea33",
        "document_id": "doc-19d46ce4",
        "document_title": "CG1x-OM0006N.pdf",
        "filename": "CG1x-OM0006N.pdf",
        "chunk_index": 0,
        "score": 0.616203,
        "metadata": {
          "filename": "CG1x-OM0006N.pdf",
          "file_type": "pdf",
          "chunk_size": 700,
          "overlap": 100,
          "start_offset": 0,
          "end_offset": 700,
          "document_id": "doc-19d46ce4",
          "chunk_id": "chk-144fe11aea33",
          "chunk_index": 0,
          "source_type": "manual"
        }
      },
      {
        "chunk_id": "chk-d185bce0f648",
        "document_id": "doc-1e985d22",
        "document_title": "CG1x-OM0006N.pdf",
        "filename": "CG1x-OM0006N.pdf",
        "chunk_index": 0,
        "score": 0.61618,
        "metadata": {
          "filename": "CG1x-OM0006N.pdf",
          "file_type": "pdf",
          "chunk_size": 700,
          "overlap": 100,
          "start_offset": 0,
          "end_offset": 700,
          "document_id": "doc-1e985d22",
          "chunk_id": "chk-d185bce0f648",
          "chunk_index": 0,
          "source_type": "manual"
        }
      },
      {
        "chunk_id": "chk-44ce5ae9159a",
        "document_id": "doc-19d46ce4",
        "document_title": "CG1x-OM0006N.pdf",
        "filename": "CG1x-OM0006N.pdf",
        "chunk_index": 27,
        "score": 0.556921,
        "metadata": {
          "filename": "CG1x-OM0006N.pdf",
          "file_type": "pdf",
          "chunk_size": 700,
          "overlap": 100,
          "start_offset": 16200,
          "end_offset": 16900,
          "document_id": "doc-19d46ce4",
          "chunk_id": "chk-44ce5ae9159a",
          "chunk_index": 27,
          "source_type": "manual"
        }
      },
      {
        "chunk_id": "chk-763a8cf76e61",
        "document_id": "doc-1e985d22",
        "document_title": "CG1x-OM0006N.pdf",
        "filename": "CG1x-OM0006N.pdf",
        "chunk_index": 27,
        "score": 0.556921,
        "metadata": {
          "filename": "CG1x-OM0006N.pdf",
          "file_type": "pdf",
          "chunk_size": 700,
          "overlap": 100,
          "start_offset": 16200,
          "end_offset": 16900,
          "document_id": "doc-1e985d22",
          "chunk_id": "chk-763a8cf76e61",
          "chunk_index": 27,
          "source_type": "manual"
        }
      }
    ],
    "operator_note": "Generated from RAG work_order_recommendation."
  },
  "work_order_quality_check": {
    "passed": true,
    "errors": [],
    "ready_to_create": false,
    "recommend_workorder": false,
    "missing_fields": []
  }
}
```

### 06. `smoke-006` [smoke]

- question_id: `smoke-006`
- type: `smoke`
- answer_overall_passed: `True`
- score: `6/6`
- should_create_workorder: `False`
- recommend_workorder: `True`
- ready_to_create: `True`
- payload_preview.fault_symptom: CG1x-OM0006N 不锈钢气缸手册包含哪些维修保养和故障对策内容？
- payload_preview.inspection_steps: `查阅手册第3章“维修保养”部分，执行3-1.点检（目录未提供具体点检项目）。, 按照3-2.密封圈的更换方法（具体步骤未在参考资料中提供）。, 参考3-3.消耗品列表（未提供具体消耗品清单）。, 依据3-4.故障与对策进行故障排查（未提供具体故障及对策）。`
- payload_preview.repair_steps: `查阅手册第3章“维修保养”部分，执行3-1.点检（目录未提供具体点检项目）。, 按照3-2.密封圈的更换方法（具体步骤未在参考资料中提供）。, 参考3-3.消耗品列表（未提供具体消耗品清单）。, 依据3-4.故障与对策进行故障排查（未提供具体故障及对策）。`
- payload_preview.key_parameters: ``
- payload_preview.safety_actions: `停止设备或相关运动。, 切断电源、气源或其他能量源。, 确认安全栅、联锁门、急停或示教器等安全装置状态。, 不允许在风险未隔离前继续操作或恢复运行。, 禁止在资料依据不足时执行高风险检修步骤。, 由受训人员或具备电气/机械维护资格的人员处理。`
- payload_preview.source_chunk_ids: `chk-144fe11aea33, chk-d185bce0f648, chk-65d6cca0f77c, chk-44ce5ae9159a, chk-763a8cf76e61`
- payload_preview.missing_fields: ``
- created_in_eval: `False`

work_order_recommendation raw:

```json
{
  "should_create_workorder": false,
  "recommend_workorder": true,
  "ready_to_create": true,
  "reason": "explicit_execution_intent",
  "explicit_execution_intent": true,
  "payload_preview": {
    "equipment_type": null,
    "fault_symptom": "CG1x-OM0006N 不锈钢气缸手册包含哪些维修保养和故障对策内容？",
    "fault_understanding": "用户询问CG1x-OM0006N不锈钢气缸手册中关于维修保养和故障对策的具体内容。根据参考资料，该手册目录显示第3章为“维修保养”，包含3-1.点检、3-2.密封圈的更换方法、3-3.消耗品、3-4.故障与对策。但参考资料仅提供目录及构造图，未给出这些章节的具体操作步骤或故障对策详细说明。",
    "possible_causes": [
      "知识库中未找到维修保养和故障对策的具体内容，仅有目录标题。"
    ],
    "repair_steps": [
      "查阅手册第3章“维修保养”部分，执行3-1.点检（目录未提供具体点检项目）。",
      "按照3-2.密封圈的更换方法（具体步骤未在参考资料中提供）。",
      "参考3-3.消耗品列表（未提供具体消耗品清单）。",
      "依据3-4.故障与对策进行故障排查（未提供具体故障及对策）。"
    ],
    "inspection_steps": [
      "查阅手册第3章“维修保养”部分，执行3-1.点检（目录未提供具体点检项目）。",
      "按照3-2.密封圈的更换方法（具体步骤未在参考资料中提供）。",
      "参考3-3.消耗品列表（未提供具体消耗品清单）。",
      "依据3-4.故障与对策进行故障排查（未提供具体故障及对策）。"
    ],
    "key_parameters": [],
    "safety_notes": [
      "所有维修保养操作前必须切断气源并释放残余压力。",
      "涉及拆装时，需使用合适工具，避免损坏不锈钢缸筒或密封件。",
      "更换密封圈等操作时，注意防止异物进入气缸内部。",
      "操作前应阅读手册“安全注意事项”部分（该部分内容未在参考资料中完整提供）。",
      "停止设备或相关运动。",
      "切断电源、气源或其他能量源。",
      "确认安全栅、联锁门、急停或示教器等安全装置状态。",
      "不允许在风险未隔离前继续操作或恢复运行。",
      "禁止在资料依据不足时执行高风险检修步骤。",
      "由受训人员或具备电气/机械维护资格的人员处理。",
      "这些注意事项，按照危害和损伤的大小及紧急程度分为「注意」 「警告」 「危险」三个等级",
      "安全注意事项 P2",
      "产品个别注意事项 P4",
      "2-2.设计注意事项",
      "3.维修保养 P16"
    ],
    "safety_actions": [
      "停止设备或相关运动。",
      "切断电源、气源或其他能量源。",
      "确认安全栅、联锁门、急停或示教器等安全装置状态。",
      "不允许在风险未隔离前继续操作或恢复运行。",
      "禁止在资料依据不足时执行高风险检修步骤。",
      "由受训人员或具备电气/机械维护资格的人员处理。"
    ],
    "source_chunk_ids": [
      "chk-144fe11aea33",
      "chk-d185bce0f648",
      "chk-65d6cca0f77c",
      "chk-44ce5ae9159a",
      "chk-763a8cf76e61"
    ],
    "missing_fields": [],
    "sources": [
      {
        "chunk_id": "chk-144fe11aea33",
        "document_id": "doc-19d46ce4",
        "document_title": "CG1x-OM0006N.pdf",
        "filename": "CG1x-OM0006N.pdf",
        "chunk_index": 0,
        "score": 0.730002,
        "metadata": {
          "filename": "CG1x-OM0006N.pdf",
          "file_type": "pdf",
          "chunk_size": 700,
          "overlap": 100,
          "start_offset": 0,
          "end_offset": 700,
          "document_id": "doc-19d46ce4",
          "chunk_id": "chk-144fe11aea33",
          "chunk_index": 0,
          "source_type": "manual"
        }
      },
      {
        "chunk_id": "chk-d185bce0f648",
        "document_id": "doc-1e985d22",
        "document_title": "CG1x-OM0006N.pdf",
        "filename": "CG1x-OM0006N.pdf",
        "chunk_index": 0,
        "score": 0.729974,
        "metadata": {
          "filename": "CG1x-OM0006N.pdf",
          "file_type": "pdf",
          "chunk_size": 700,
          "overlap": 100,
          "start_offset": 0,
          "end_offset": 700,
          "document_id": "doc-1e985d22",
          "chunk_id": "chk-d185bce0f648",
          "chunk_index": 0,
          "source_type": "manual"
        }
      },
      {
        "chunk_id": "chk-65d6cca0f77c",
        "document_id": "doc-bc2d279f",
        "document_title": "CM2x-OM0230Q.pdf",
        "filename": "CM2x-OM0230Q.pdf",
        "chunk_index": 0,
        "score": 0.664283,
        "metadata": {
          "filename": "CM2x-OM0230Q.pdf",
          "file_type": "pdf",
          "chunk_size": 700,
          "overlap": 100,
          "start_offset": 0,
          "end_offset": 700,
          "document_id": "doc-bc2d279f",
          "chunk_id": "chk-65d6cca0f77c",
          "chunk_index": 0,
          "source_type": "manual"
        }
      },
      {
        "chunk_id": "chk-44ce5ae9159a",
        "document_id": "doc-19d46ce4",
        "document_title": "CG1x-OM0006N.pdf",
        "filename": "CG1x-OM0006N.pdf",
        "chunk_index": 27,
        "score": 0.611462,
        "metadata": {
          "filename": "CG1x-OM0006N.pdf",
          "file_type": "pdf",
          "chunk_size": 700,
          "overlap": 100,
          "start_offset": 16200,
          "end_offset": 16900,
          "document_id": "doc-19d46ce4",
          "chunk_id": "chk-44ce5ae9159a",
          "chunk_index": 27,
          "source_type": "manual"
        }
      },
      {
        "chunk_id": "chk-763a8cf76e61",
        "document_id": "doc-1e985d22",
        "document_title": "CG1x-OM0006N.pdf",
        "filename": "CG1x-OM0006N.pdf",
        "chunk_index": 27,
        "score": 0.611462,
        "metadata": {
          "filename": "CG1x-OM0006N.pdf",
          "file_type": "pdf",
          "chunk_size": 700,
          "overlap": 100,
          "start_offset": 16200,
          "end_offset": 16900,
          "document_id": "doc-1e985d22",
          "chunk_id": "chk-763a8cf76e61",
          "chunk_index": 27,
          "source_type": "manual"
        }
      }
    ],
    "operator_note": "Generated from RAG work_order_recommendation."
  },
  "work_order_quality_check": {
    "passed": true,
    "errors": [],
    "ready_to_create": true,
    "recommend_workorder": true,
    "missing_fields": []
  }
}
```

### 07. `param-001` [parameter]

- question_id: `param-001`
- type: `parameter`
- answer_overall_passed: `True`
- score: `6/6`
- should_create_workorder: `False`
- recommend_workorder: `False`
- ready_to_create: `False`
- payload_preview.fault_symptom: 摩托车发动机火花塞间隙标准值是多少？安装火花塞的拧紧力矩是多少？
- payload_preview.inspection_steps: `1. 使用塞尺测量火花塞间隙，标准值为0.7～0.9 mm，超出范围须更换火花塞。, 2. 安装火花塞：将火花塞放入气缸头，套上火花塞专用套筒，顺时针转动3圈预紧。, 3. 然后继续转动1/4圈，或使用定扭扳手拧紧至20 ± 2 N·m。, 4. 用尖嘴钳将高压帽套进火花塞并用力往下压紧。`
- payload_preview.repair_steps: `1. 使用塞尺测量火花塞间隙，标准值为0.7～0.9 mm，超出范围须更换火花塞。, 2. 安装火花塞：将火花塞放入气缸头，套上火花塞专用套筒，顺时针转动3圈预紧。, 3. 然后继续转动1/4圈，或使用定扭扳手拧紧至20 ± 2 N·m。, 4. 用尖嘴钳将高压帽套进火花塞并用力往下压紧。`
- payload_preview.key_parameters: `0.7, 0.9, 20, N·m`
- payload_preview.safety_actions: ``
- payload_preview.source_chunk_ids: `chk-21541424d16a, chk-d026f9ac3955, chk-dfb84876691d, chk-4d7f935536ae, chk-ab08fbdb930b`
- payload_preview.missing_fields: ``
- created_in_eval: `False`
- 未 ready_to_create 原因: reason=no_workorder_intent_detected

work_order_recommendation raw:

```json
{
  "should_create_workorder": false,
  "recommend_workorder": false,
  "ready_to_create": false,
  "reason": "no_workorder_intent_detected",
  "explicit_execution_intent": false,
  "payload_preview": {
    "equipment_type": null,
    "fault_symptom": "摩托车发动机火花塞间隙标准值是多少？安装火花塞的拧紧力矩是多少？",
    "fault_understanding": "用户询问摩托车发动机火花塞间隙标准值及安装拧紧力矩，参考资料中提供了明确数据。",
    "possible_causes": [],
    "repair_steps": [
      "1. 使用塞尺测量火花塞间隙，标准值为0.7～0.9 mm，超出范围须更换火花塞。",
      "2. 安装火花塞：将火花塞放入气缸头，套上火花塞专用套筒，顺时针转动3圈预紧。",
      "3. 然后继续转动1/4圈，或使用定扭扳手拧紧至20 ± 2 N·m。",
      "4. 用尖嘴钳将高压帽套进火花塞并用力往下压紧。"
    ],
    "inspection_steps": [
      "1. 使用塞尺测量火花塞间隙，标准值为0.7～0.9 mm，超出范围须更换火花塞。",
      "2. 安装火花塞：将火花塞放入气缸头，套上火花塞专用套筒，顺时针转动3圈预紧。",
      "3. 然后继续转动1/4圈，或使用定扭扳手拧紧至20 ± 2 N·m。",
      "4. 用尖嘴钳将高压帽套进火花塞并用力往下压紧。"
    ],
    "key_parameters": [
      "0.7",
      "0.9",
      "20",
      "N·m"
    ],
    "safety_notes": [
      "在拆卸火花塞之前要确保火花塞孔及其周围没有灰尘。",
      "安装火花塞时使用专用套筒，避免损坏火花塞或气缸头。",
      "拧紧力矩不得超过规定范围，以免损坏螺纹或火花塞。"
    ],
    "safety_actions": [],
    "source_chunk_ids": [
      "chk-21541424d16a",
      "chk-d026f9ac3955",
      "chk-dfb84876691d",
      "chk-4d7f935536ae",
      "chk-ab08fbdb930b"
    ],
    "missing_fields": [],
    "sources": [
      {
        "chunk_id": "chk-21541424d16a",
        "document_id": "doc-5a5e4729",
        "document_title": "摩托车发动机维修手册.pdf",
        "filename": "摩托车发动机维修手册.pdf",
        "chunk_index": 2,
        "score": 0.747561,
        "metadata": {
          "filename": "摩托车发动机维修手册.pdf",
          "file_type": "pdf",
          "chunk_size": 700,
          "overlap": 100,
          "start_offset": 1200,
          "end_offset": 1900,
          "document_id": "doc-5a5e4729",
          "chunk_id": "chk-21541424d16a",
          "chunk_index": 2,
          "source_type": "manual"
        }
      },
      {
        "chunk_id": "chk-d026f9ac3955",
        "document_id": "doc-5a5e4729",
        "document_title": "摩托车发动机维修手册.pdf",
        "filename": "摩托车发动机维修手册.pdf",
        "chunk_index": 6,
        "score": 0.653299,
        "metadata": {
          "filename": "摩托车发动机维修手册.pdf",
          "file_type": "pdf",
          "chunk_size": 700,
          "overlap": 100,
          "start_offset": 3600,
          "end_offset": 4300,
          "document_id": "doc-5a5e4729",
          "chunk_id": "chk-d026f9ac3955",
          "chunk_index": 6,
          "source_type": "manual"
        }
      },
      {
        "chunk_id": "chk-dfb84876691d",
        "document_id": "doc-5a5e4729",
        "document_title": "摩托车发动机维修手册.pdf",
        "filename": "摩托车发动机维修手册.pdf",
        "chunk_index": 5,
        "score": 0.634031,
        "metadata": {
          "filename": "摩托车发动机维修手册.pdf",
          "file_type": "pdf",
          "chunk_size": 700,
          "overlap": 100,
          "start_offset": 3000,
          "end_offset": 3700,
          "document_id": "doc-5a5e4729",
          "chunk_id": "chk-dfb84876691d",
          "chunk_index": 5,
          "source_type": "manual"
        }
      },
      {
        "chunk_id": "chk-4d7f935536ae",
        "document_id": "doc-5a5e4729",
        "document_title": "摩托车发动机维修手册.pdf",
        "filename": "摩托车发动机维修手册.pdf",
        "chunk_index": 13,
        "score": 0.632085,
        "metadata": {
          "filename": "摩托车发动机维修手册.pdf",
          "file_type": "pdf",
          "chunk_size": 700,
          "overlap": 100,
          "start_offset": 7800,
          "end_offset": 8500,
          "document_id": "doc-5a5e4729",
          "chunk_id": "chk-4d7f935536ae",
          "chunk_index": 13,
          "source_type": "manual"
        }
      },
      {
        "chunk_id": "chk-ab08fbdb930b",
        "document_id": "doc-5a5e4729",
        "document_title": "摩托车发动机维修手册.pdf",
        "filename": "摩托车发动机维修手册.pdf",
        "chunk_index": 9,
        "score": 0.631945,
        "metadata": {
          "filename": "摩托车发动机维修手册.pdf",
          "file_type": "pdf",
          "chunk_size": 700,
          "overlap": 100,
          "start_offset": 5400,
          "end_offset": 6100,
          "document_id": "doc-5a5e4729",
          "chunk_id": "chk-ab08fbdb930b",
          "chunk_index": 9,
          "source_type": "manual"
        }
      }
    ],
    "operator_note": "Generated from RAG work_order_recommendation."
  },
  "work_order_quality_check": {
    "passed": true,
    "errors": [],
    "ready_to_create": false,
    "recommend_workorder": false,
    "missing_fields": []
  }
}
```

### 08. `param-002` [parameter]

- question_id: `param-002`
- type: `parameter`
- answer_overall_passed: `True`
- score: `6/6`
- should_create_workorder: `False`
- recommend_workorder: `False`
- ready_to_create: `False`
- payload_preview.fault_symptom: 摩托车发动机测量压缩压力时，标准压缩压力范围是多少？
- payload_preview.inspection_steps: `启动发动机预热几分钟后熄火。, 拆卸火花塞，确保火花塞孔及其周围无灰尘。, 安装压力表。, 将油门开到最大，用启动电机带动发动机转动，直至压力表读数稳定。, 注意：在启动发动机之前，将燃油喷射器拆卸下来。, 若压缩压力异常，根据结果分析进行相应检查和更换。`
- payload_preview.repair_steps: `启动发动机预热几分钟后熄火。, 拆卸火花塞，确保火花塞孔及其周围无灰尘。, 安装压力表。, 将油门开到最大，用启动电机带动发动机转动，直至压力表读数稳定。, 注意：在启动发动机之前，将燃油喷射器拆卸下来。, 若压缩压力异常，根据结果分析进行相应检查和更换。`
- payload_preview.key_parameters: `1300, 1900, 500, 900, kPa`
- payload_preview.safety_actions: `停止设备或相关运动。, 切断电源、气源或其他能量源。, 确认安全栅、联锁门、急停或示教器等安全装置状态。, 检查火花塞孔周围清洁度。, 拆卸燃油喷射器。, 拆卸火花塞并安装压力表。, 不允许在风险未隔离前继续操作或恢复运行。, 禁止在资料依据不足时执行高风险检修步骤。, 不允许在未清理灰尘或未拆卸燃油喷射器的情况下进行压缩压力测量。, 由受训人员或具备电气/机械维护资格的人员处理。`
- payload_preview.source_chunk_ids: `chk-21541424d16a, chk-d026f9ac3955, chk-dfb84876691d, chk-4896a18d171f, chk-724a5de67b0b`
- payload_preview.missing_fields: ``
- created_in_eval: `False`
- 未 ready_to_create 原因: reason=no_workorder_intent_detected

work_order_recommendation raw:

```json
{
  "should_create_workorder": false,
  "recommend_workorder": false,
  "ready_to_create": false,
  "reason": "no_workorder_intent_detected",
  "explicit_execution_intent": false,
  "payload_preview": {
    "equipment_type": null,
    "fault_symptom": "摩托车发动机测量压缩压力时，标准压缩压力范围是多少？",
    "fault_understanding": "用户询问摩托车发动机标准压缩压力范围，手册中明确给出了具体数值：1300～1900 kPa（1500 r/min）和500～900 kPa（540 r/min）。",
    "possible_causes": [],
    "repair_steps": [
      "启动发动机预热几分钟后熄火。",
      "拆卸火花塞，确保火花塞孔及其周围无灰尘。",
      "安装压力表。",
      "将油门开到最大，用启动电机带动发动机转动，直至压力表读数稳定。",
      "注意：在启动发动机之前，将燃油喷射器拆卸下来。",
      "若压缩压力异常，根据结果分析进行相应检查和更换。"
    ],
    "inspection_steps": [
      "启动发动机预热几分钟后熄火。",
      "拆卸火花塞，确保火花塞孔及其周围无灰尘。",
      "安装压力表。",
      "将油门开到最大，用启动电机带动发动机转动，直至压力表读数稳定。",
      "注意：在启动发动机之前，将燃油喷射器拆卸下来。",
      "若压缩压力异常，根据结果分析进行相应检查和更换。"
    ],
    "key_parameters": [
      "1300",
      "1900",
      "500",
      "900",
      "kPa"
    ],
    "safety_notes": [
      "停止设备或相关运动。",
      "切断电源、气源或其他能量源。",
      "确认安全栅、联锁门、急停或示教器等安全装置状态。",
      "不允许在风险未隔离前继续操作或恢复运行。",
      "禁止在资料依据不足时执行高风险检修步骤。",
      "由受训人员或具备电气/机械维护资格的人员处理。",
      "所有螺栓安装后，必须使用扭力扳手校验并打紧至规定扭矩",
      "警告",
      "压缩空气中不得含有化学药品、有机溶剂的合成油、盐分、腐蚀性气体等，以免造成产品破损及",
      "摩托车发动机维修手册.pdf",
      "，若有损坏或变形，则应更换火花塞",
      "拆卸火花塞前必须确保火花塞孔及其周围没有灰尘。",
      "在启动发动机之前，必须将燃油喷射器拆卸下来。",
      "所有螺栓安装后，必须使用扭力扳手校验并打紧至规定扭矩（来自手册其他部分，但保留作为通用安全提醒）。",
      "检查火花塞孔周围清洁度。",
      "拆卸燃油喷射器。",
      "拆卸火花塞并安装压力表。",
      "不允许在未清理灰尘或未拆卸燃油喷射器的情况下进行压缩压力测量。",
      "标准压缩压力范围：1300 ～ 1900 kPa（转速：1500 r/min ）500 ～ 900 kPa（转速：540 r/min ）",
      "注意：在拆卸火花塞之前要确保火花塞孔及其周围没有灰尘。",
      "警示：在启动发动机之前，将燃油喷射器拆卸下来。"
    ],
    "safety_actions": [
      "停止设备或相关运动。",
      "切断电源、气源或其他能量源。",
      "确认安全栅、联锁门、急停或示教器等安全装置状态。",
      "检查火花塞孔周围清洁度。",
      "拆卸燃油喷射器。",
      "拆卸火花塞并安装压力表。",
      "不允许在风险未隔离前继续操作或恢复运行。",
      "禁止在资料依据不足时执行高风险检修步骤。",
      "不允许在未清理灰尘或未拆卸燃油喷射器的情况下进行压缩压力测量。",
      "由受训人员或具备电气/机械维护资格的人员处理。"
    ],
    "source_chunk_ids": [
      "chk-21541424d16a",
      "chk-d026f9ac3955",
      "chk-dfb84876691d",
      "chk-4896a18d171f",
      "chk-724a5de67b0b"
    ],
    "missing_fields": [],
    "sources": [
      {
        "chunk_id": "chk-21541424d16a",
        "document_id": "doc-5a5e4729",
        "document_title": "摩托车发动机维修手册.pdf",
        "filename": "摩托车发动机维修手册.pdf",
        "chunk_index": 2,
        "score": 0.687767,
        "metadata": {
          "filename": "摩托车发动机维修手册.pdf",
          "file_type": "pdf",
          "chunk_size": 700,
          "overlap": 100,
          "start_offset": 1200,
          "end_offset": 1900,
          "document_id": "doc-5a5e4729",
          "chunk_id": "chk-21541424d16a",
          "chunk_index": 2,
          "source_type": "manual"
        }
      },
      {
        "chunk_id": "chk-d026f9ac3955",
        "document_id": "doc-5a5e4729",
        "document_title": "摩托车发动机维修手册.pdf",
        "filename": "摩托车发动机维修手册.pdf",
        "chunk_index": 6,
        "score": 0.621322,
        "metadata": {
          "filename": "摩托车发动机维修手册.pdf",
          "file_type": "pdf",
          "chunk_size": 700,
          "overlap": 100,
          "start_offset": 3600,
          "end_offset": 4300,
          "document_id": "doc-5a5e4729",
          "chunk_id": "chk-d026f9ac3955",
          "chunk_index": 6,
          "source_type": "manual"
        }
      },
      {
        "chunk_id": "chk-dfb84876691d",
        "document_id": "doc-5a5e4729",
        "document_title": "摩托车发动机维修手册.pdf",
        "filename": "摩托车发动机维修手册.pdf",
        "chunk_index": 5,
        "score": 0.610289,
        "metadata": {
          "filename": "摩托车发动机维修手册.pdf",
          "file_type": "pdf",
          "chunk_size": 700,
          "overlap": 100,
          "start_offset": 3000,
          "end_offset": 3700,
          "document_id": "doc-5a5e4729",
          "chunk_id": "chk-dfb84876691d",
          "chunk_index": 5,
          "source_type": "manual"
        }
      },
      {
        "chunk_id": "chk-4896a18d171f",
        "document_id": "doc-19d46ce4",
        "document_title": "CG1x-OM0006N.pdf",
        "filename": "CG1x-OM0006N.pdf",
        "chunk_index": 8,
        "score": 0.602476,
        "metadata": {
          "filename": "CG1x-OM0006N.pdf",
          "file_type": "pdf",
          "chunk_size": 700,
          "overlap": 100,
          "start_offset": 4800,
          "end_offset": 5500,
          "document_id": "doc-19d46ce4",
          "chunk_id": "chk-4896a18d171f",
          "chunk_index": 8,
          "source_type": "manual"
        }
      },
      {
        "chunk_id": "chk-724a5de67b0b",
        "document_id": "doc-1e985d22",
        "document_title": "CG1x-OM0006N.pdf",
        "filename": "CG1x-OM0006N.pdf",
        "chunk_index": 8,
        "score": 0.602476,
        "metadata": {
          "filename": "CG1x-OM0006N.pdf",
          "file_type": "pdf",
          "chunk_size": 700,
          "overlap": 100,
          "start_offset": 4800,
          "end_offset": 5500,
          "document_id": "doc-1e985d22",
          "chunk_id": "chk-724a5de67b0b",
          "chunk_index": 8,
          "source_type": "manual"
        }
      }
    ],
    "operator_note": "Generated from RAG work_order_recommendation."
  },
  "work_order_quality_check": {
    "passed": true,
    "errors": [],
    "ready_to_create": false,
    "recommend_workorder": false,
    "missing_fields": []
  }
}
```

### 09. `param-003` [parameter]

- question_id: `param-003`
- type: `parameter`
- answer_overall_passed: `True`
- score: `6/6`
- should_create_workorder: `False`
- recommend_workorder: `False`
- ready_to_create: `False`
- payload_preview.fault_symptom: CM2 系列气缸使用前需要确认哪些空气源和速度控制相关条件？
- payload_preview.inspection_steps: `1. 空气源确认：配管前对气管和接头进行吹净或充分清洗，彻底清除切削末、切削油、粉尘等异物。, 2. 密封带缠绕：拧入配管或管接头时，避免切削末或密封材进入配管内部；使用密封带时，螺纹前端留出1.5~2个螺牙不缠。, 3. 速度控制确认：在气缸供气口安装速度控制阀（如AS系列），通常采用排气节流控制方式。, 4. 速度调整：将调速阀完全关闭，从低速开始逐渐调整到指定速度。, 5. 确认设备作动正常：连接气源和电气后，进行功能检查和泄漏检查，确认安装正确。`
- payload_preview.repair_steps: `1. 空气源确认：配管前对气管和接头进行吹净或充分清洗，彻底清除切削末、切削油、粉尘等异物。, 2. 密封带缠绕：拧入配管或管接头时，避免切削末或密封材进入配管内部；使用密封带时，螺纹前端留出1.5~2个螺牙不缠。, 3. 速度控制确认：在气缸供气口安装速度控制阀（如AS系列），通常采用排气节流控制方式。, 4. 速度调整：将调速阀完全关闭，从低速开始逐渐调整到指定速度。, 5. 确认设备作动正常：连接气源和电气后，进行功能检查和泄漏检查，确认安装正确。`
- payload_preview.key_parameters: ``
- payload_preview.safety_actions: `停止设备或相关运动。, 切断电源、气源或其他能量源。, 确认安全栅、联锁门、急停或示教器等安全装置状态。, 不允许在风险未隔离前继续操作或恢复运行。, 禁止在资料依据不足时执行高风险检修步骤。, 由受训人员或具备电气/机械维护资格的人员处理。`
- payload_preview.source_chunk_ids: `chk-65d6cca0f77c, chk-8bb7d4bc9b80, chk-647729f3f513, chk-730b481cb2cb, chk-bcaa8d1cf42c`
- payload_preview.missing_fields: ``
- created_in_eval: `False`
- 未 ready_to_create 原因: reason=no_workorder_intent_detected

work_order_recommendation raw:

```json
{
  "should_create_workorder": false,
  "recommend_workorder": false,
  "ready_to_create": false,
  "reason": "no_workorder_intent_detected",
  "explicit_execution_intent": false,
  "payload_preview": {
    "equipment_type": null,
    "fault_symptom": "CM2 系列气缸使用前需要确认哪些空气源和速度控制相关条件？",
    "fault_understanding": "用户询问CM2系列气缸使用前需要确认的空气源和速度控制相关条件。参考资料中CM2系列说明书仅有目录，未提供具体章节内容；但CG1系列说明书中包含类似通用的使用空气和速度控制要求，可作为参考。知识库中未找到CM2系列对此问题的充分依据。",
    "possible_causes": [
      "参考资料中CM2系列说明书内容不完整，无法直接提取空气源和速度控制条件。",
      "CG1系列说明书中建议：空气源需进行配管前吹净或清洗，清除管内切削末、切削油、粉尘等；速度控制需在气缸供气口安装速度控制阀，通常采用排气节流控制方式，调整时从调速阀全闭状态开始逐渐增至指定速度。"
    ],
    "repair_steps": [
      "1. 空气源确认：配管前对气管和接头进行吹净或充分清洗，彻底清除切削末、切削油、粉尘等异物。",
      "2. 密封带缠绕：拧入配管或管接头时，避免切削末或密封材进入配管内部；使用密封带时，螺纹前端留出1.5~2个螺牙不缠。",
      "3. 速度控制确认：在气缸供气口安装速度控制阀（如AS系列），通常采用排气节流控制方式。",
      "4. 速度调整：将调速阀完全关闭，从低速开始逐渐调整到指定速度。",
      "5. 确认设备作动正常：连接气源和电气后，进行功能检查和泄漏检查，确认安装正确。"
    ],
    "inspection_steps": [
      "1. 空气源确认：配管前对气管和接头进行吹净或充分清洗，彻底清除切削末、切削油、粉尘等异物。",
      "2. 密封带缠绕：拧入配管或管接头时，避免切削末或密封材进入配管内部；使用密封带时，螺纹前端留出1.5~2个螺牙不缠。",
      "3. 速度控制确认：在气缸供气口安装速度控制阀（如AS系列），通常采用排气节流控制方式。",
      "4. 速度调整：将调速阀完全关闭，从低速开始逐渐调整到指定速度。",
      "5. 确认设备作动正常：连接气源和电气后，进行功能检查和泄漏检查，确认安装正确。"
    ],
    "key_parameters": [],
    "safety_notes": [
      "1. 速度调整时必须从调速阀全闭状态开始，逐渐增加，防止气缸突然高速动作造成危险。",
      "2. 配管前必须彻底清除管内的切削末、切削油、粉尘等杂质，避免进入气缸内部导致密封件损伤。",
      "3. 使用密封带时注意缠绕方向，防止密封材料进入配管内部。",
      "4. 在确认设备作动正常前不得投入使用，应进行必要的功能检查及泄漏检查。",
      "停止设备或相关运动。",
      "切断电源、气源或其他能量源。",
      "确认安全栅、联锁门、急停或示教器等安全装置状态。",
      "不允许在风险未隔离前继续操作或恢复运行。",
      "禁止在资料依据不足时执行高风险检修步骤。",
      "由受训人员或具备电气/机械维护资格的人员处理。",
      "这种情况必须十分注意",
      "警告",
      "安全注意事项 P2",
      "2-2. 设计注意事项",
      "3-1. 活塞杆密封圈的更换方法"
    ],
    "safety_actions": [
      "停止设备或相关运动。",
      "切断电源、气源或其他能量源。",
      "确认安全栅、联锁门、急停或示教器等安全装置状态。",
      "不允许在风险未隔离前继续操作或恢复运行。",
      "禁止在资料依据不足时执行高风险检修步骤。",
      "由受训人员或具备电气/机械维护资格的人员处理。"
    ],
    "source_chunk_ids": [
      "chk-65d6cca0f77c",
      "chk-8bb7d4bc9b80",
      "chk-647729f3f513",
      "chk-730b481cb2cb",
      "chk-bcaa8d1cf42c"
    ],
    "missing_fields": [],
    "sources": [
      {
        "chunk_id": "chk-65d6cca0f77c",
        "document_id": "doc-bc2d279f",
        "document_title": "CM2x-OM0230Q.pdf",
        "filename": "CM2x-OM0230Q.pdf",
        "chunk_index": 0,
        "score": 0.669675,
        "metadata": {
          "filename": "CM2x-OM0230Q.pdf",
          "file_type": "pdf",
          "chunk_size": 700,
          "overlap": 100,
          "start_offset": 0,
          "end_offset": 700,
          "document_id": "doc-bc2d279f",
          "chunk_id": "chk-65d6cca0f77c",
          "chunk_index": 0,
          "source_type": "manual"
        }
      },
      {
        "chunk_id": "chk-8bb7d4bc9b80",
        "document_id": "doc-19d46ce4",
        "document_title": "CG1x-OM0006N.pdf",
        "filename": "CG1x-OM0006N.pdf",
        "chunk_index": 14,
        "score": 0.623545,
        "metadata": {
          "filename": "CG1x-OM0006N.pdf",
          "file_type": "pdf",
          "chunk_size": 700,
          "overlap": 100,
          "start_offset": 8400,
          "end_offset": 9100,
          "document_id": "doc-19d46ce4",
          "chunk_id": "chk-8bb7d4bc9b80",
          "chunk_index": 14,
          "source_type": "manual"
        }
      },
      {
        "chunk_id": "chk-647729f3f513",
        "document_id": "doc-1e985d22",
        "document_title": "CG1x-OM0006N.pdf",
        "filename": "CG1x-OM0006N.pdf",
        "chunk_index": 14,
        "score": 0.623545,
        "metadata": {
          "filename": "CG1x-OM0006N.pdf",
          "file_type": "pdf",
          "chunk_size": 700,
          "overlap": 100,
          "start_offset": 8400,
          "end_offset": 9100,
          "document_id": "doc-1e985d22",
          "chunk_id": "chk-647729f3f513",
          "chunk_index": 14,
          "source_type": "manual"
        }
      },
      {
        "chunk_id": "chk-730b481cb2cb",
        "document_id": "doc-19d46ce4",
        "document_title": "CG1x-OM0006N.pdf",
        "filename": "CG1x-OM0006N.pdf",
        "chunk_index": 15,
        "score": 0.619911,
        "metadata": {
          "filename": "CG1x-OM0006N.pdf",
          "file_type": "pdf",
          "chunk_size": 700,
          "overlap": 100,
          "start_offset": 9000,
          "end_offset": 9700,
          "document_id": "doc-19d46ce4",
          "chunk_id": "chk-730b481cb2cb",
          "chunk_index": 15,
          "source_type": "manual"
        }
      },
      {
        "chunk_id": "chk-bcaa8d1cf42c",
        "document_id": "doc-1e985d22",
        "document_title": "CG1x-OM0006N.pdf",
        "filename": "CG1x-OM0006N.pdf",
        "chunk_index": 15,
        "score": 0.619911,
        "metadata": {
          "filename": "CG1x-OM0006N.pdf",
          "file_type": "pdf",
          "chunk_size": 700,
          "overlap": 100,
          "start_offset": 9000,
          "end_offset": 9700,
          "document_id": "doc-1e985d22",
          "chunk_id": "chk-bcaa8d1cf42c",
          "chunk_index": 15,
          "source_type": "manual"
        }
      }
    ],
    "operator_note": "Generated from RAG work_order_recommendation."
  },
  "work_order_quality_check": {
    "passed": true,
    "errors": [],
    "ready_to_create": false,
    "recommend_workorder": false,
    "missing_fields": []
  }
}
```

### 10. `param-004` [parameter]

- question_id: `param-004`
- type: `parameter`
- answer_overall_passed: `True`
- score: `6/6`
- should_create_workorder: `False`
- recommend_workorder: `False`
- ready_to_create: `False`
- payload_preview.fault_symptom: CG1 系列不锈钢气缸磁性开关安装时，安装螺钉的紧固力矩要求是什么？
- payload_preview.inspection_steps: `根据参考资料，M4 螺钉的紧固力矩为 1~1.2 N·m。`
- payload_preview.repair_steps: `根据参考资料，M4 螺钉的紧固力矩为 1~1.2 N·m。`
- payload_preview.key_parameters: `M4, 1, 1.2, N`
- payload_preview.safety_actions: ``
- payload_preview.source_chunk_ids: `chk-c1f980dc39dd, chk-e3133442503d, chk-a22f19291795, chk-65a4ebe4d849, chk-2fdc017d9509`
- payload_preview.missing_fields: ``
- created_in_eval: `False`
- 未 ready_to_create 原因: reason=no_workorder_intent_detected

work_order_recommendation raw:

```json
{
  "should_create_workorder": false,
  "recommend_workorder": false,
  "ready_to_create": false,
  "reason": "no_workorder_intent_detected",
  "explicit_execution_intent": false,
  "payload_preview": {
    "equipment_type": null,
    "fault_symptom": "CG1 系列不锈钢气缸磁性开关安装时，安装螺钉的紧固力矩要求是什么？",
    "fault_understanding": "用户询问 CG1 系列不锈钢气缸磁性开关安装螺钉的紧固力矩要求，参考资料中明确给出了 M4 螺钉的力矩范围。",
    "possible_causes": [],
    "repair_steps": [
      "根据参考资料，M4 螺钉的紧固力矩为 1~1.2 N·m。"
    ],
    "inspection_steps": [
      "根据参考资料，M4 螺钉的紧固力矩为 1~1.2 N·m。"
    ],
    "key_parameters": [
      "M4",
      "1",
      "1.2",
      "N"
    ],
    "safety_notes": [
      "紧固时请使用扭矩扳手，避免力矩过大损坏螺纹或导致磁性开关变形，力矩过小则可能固定不牢。",
      "在安装前应确保气缸已切断气源和电源，并排空系统内残余压缩空气，防止误动作。"
    ],
    "safety_actions": [],
    "source_chunk_ids": [
      "chk-c1f980dc39dd",
      "chk-e3133442503d",
      "chk-a22f19291795",
      "chk-65a4ebe4d849",
      "chk-2fdc017d9509"
    ],
    "missing_fields": [],
    "sources": [
      {
        "chunk_id": "chk-c1f980dc39dd",
        "document_id": "doc-19d46ce4",
        "document_title": "CG1x-OM0006N.pdf",
        "filename": "CG1x-OM0006N.pdf",
        "chunk_index": 19,
        "score": 0.701549,
        "metadata": {
          "filename": "CG1x-OM0006N.pdf",
          "file_type": "pdf",
          "chunk_size": 700,
          "overlap": 100,
          "start_offset": 11400,
          "end_offset": 12100,
          "document_id": "doc-19d46ce4",
          "chunk_id": "chk-c1f980dc39dd",
          "chunk_index": 19,
          "source_type": "manual"
        }
      },
      {
        "chunk_id": "chk-e3133442503d",
        "document_id": "doc-1e985d22",
        "document_title": "CG1x-OM0006N.pdf",
        "filename": "CG1x-OM0006N.pdf",
        "chunk_index": 19,
        "score": 0.701549,
        "metadata": {
          "filename": "CG1x-OM0006N.pdf",
          "file_type": "pdf",
          "chunk_size": 700,
          "overlap": 100,
          "start_offset": 11400,
          "end_offset": 12100,
          "document_id": "doc-1e985d22",
          "chunk_id": "chk-e3133442503d",
          "chunk_index": 19,
          "source_type": "manual"
        }
      },
      {
        "chunk_id": "chk-a22f19291795",
        "document_id": "doc-bc2d279f",
        "document_title": "CM2x-OM0230Q.pdf",
        "filename": "CM2x-OM0230Q.pdf",
        "chunk_index": 11,
        "score": 0.677918,
        "metadata": {
          "filename": "CM2x-OM0230Q.pdf",
          "file_type": "pdf",
          "chunk_size": 700,
          "overlap": 100,
          "start_offset": 6600,
          "end_offset": 7300,
          "document_id": "doc-bc2d279f",
          "chunk_id": "chk-a22f19291795",
          "chunk_index": 11,
          "source_type": "manual"
        }
      },
      {
        "chunk_id": "chk-65a4ebe4d849",
        "document_id": "doc-19d46ce4",
        "document_title": "CG1x-OM0006N.pdf",
        "filename": "CG1x-OM0006N.pdf",
        "chunk_index": 18,
        "score": 0.670753,
        "metadata": {
          "filename": "CG1x-OM0006N.pdf",
          "file_type": "pdf",
          "chunk_size": 700,
          "overlap": 100,
          "start_offset": 10800,
          "end_offset": 11500,
          "document_id": "doc-19d46ce4",
          "chunk_id": "chk-65a4ebe4d849",
          "chunk_index": 18,
          "source_type": "manual"
        }
      },
      {
        "chunk_id": "chk-2fdc017d9509",
        "document_id": "doc-1e985d22",
        "document_title": "CG1x-OM0006N.pdf",
        "filename": "CG1x-OM0006N.pdf",
        "chunk_index": 18,
        "score": 0.670753,
        "metadata": {
          "filename": "CG1x-OM0006N.pdf",
          "file_type": "pdf",
          "chunk_size": 700,
          "overlap": 100,
          "start_offset": 10800,
          "end_offset": 11500,
          "document_id": "doc-1e985d22",
          "chunk_id": "chk-2fdc017d9509",
          "chunk_index": 18,
          "source_type": "manual"
        }
      }
    ],
    "operator_note": "Generated from RAG work_order_recommendation."
  },
  "work_order_quality_check": {
    "passed": true,
    "errors": [],
    "ready_to_create": false,
    "recommend_workorder": false,
    "missing_fields": []
  }
}
```

### 11. `param-005` [parameter]

- question_id: `param-005`
- type: `parameter`
- answer_overall_passed: `True`
- score: `6/6`
- should_create_workorder: `False`
- recommend_workorder: `False`
- ready_to_create: `False`
- payload_preview.fault_symptom: FANUC 机器人控制器相关安全功能中，Emergency stop、mode select switch、deadman switch 分别属于哪些安全控制主题？
- payload_preview.inspection_steps: `根据参考资料，这些设备的功能已在安全手册中描述：Emergency stop 用于紧急停止（参见 SRVO-001 和 SRVO-002 报警）；deadman switch 在 T1/T2 模式下作为使能装置（参见片段1）；mode select switch 用于选择运行模式（AUTO/T1/T2），影响停止模式（参见片段2表格）。, 如需更精确的归类，建议查阅 FANUC 控制器的操作手册或相关安全标准（如 ISO 13849）中关于安全功能主题的定义。`
- payload_preview.repair_steps: `根据参考资料，这些设备的功能已在安全手册中描述：Emergency stop 用于紧急停止（参见 SRVO-001 和 SRVO-002 报警）；deadman switch 在 T1/T2 模式下作为使能装置（参见片段1）；mode select switch 用于选择运行模式（AUTO/T1/T2），影响停止模式（参见片段2表格）。, 如需更精确的归类，建议查阅 FANUC 控制器的操作手册或相关安全标准（如 ISO 13849）中关于安全功能主题的定义。`
- payload_preview.key_parameters: `Emergency stop, mode select, deadman, teach pendant`
- payload_preview.safety_actions: `停止设备或相关运动。, 切断电源、气源或其他能量源。, 确认安全栅、联锁门、急停或示教器等安全装置状态。, 不允许在风险未隔离前继续操作或恢复运行。, 禁止在资料依据不足时执行高风险检修步骤。, 由受训人员或具备电气/机械维护资格的人员处理。`
- payload_preview.source_chunk_ids: `chk-97c9bf4b7bb0, chk-11932d0c1547, chk-a5646801d304, chk-03d68abdce49, chk-433ca6a8c08f`
- payload_preview.missing_fields: ``
- created_in_eval: `False`
- 未 ready_to_create 原因: reason=no_workorder_intent_detected

work_order_recommendation raw:

```json
{
  "should_create_workorder": false,
  "recommend_workorder": false,
  "ready_to_create": false,
  "reason": "no_workorder_intent_detected",
  "explicit_execution_intent": false,
  "payload_preview": {
    "equipment_type": null,
    "fault_symptom": "FANUC 机器人控制器相关安全功能中，Emergency stop、mode select switch、deadman switch 分别属于哪些安全控制主题？",
    "fault_understanding": "用户询问FANUC机器人控制器中Emergency stop、mode select switch和deadman switch分别属于哪些安全控制主题。参考资料中将这些设备统称为“SAFETY DEVICES”（安全装置），但未明确区分更细的安全控制主题。资料片段中未检索到该项的充分依据。",
    "possible_causes": [
      "参考资料中未明确定义 '安全控制主题' 的分类体系，仅将上述设备统称为安全装置。",
      "参考资料中未定义“安全控制主题”的分类体系，仅将上述设备统称为安全装置。"
    ],
    "repair_steps": [
      "根据参考资料，这些设备的功能已在安全手册中描述：Emergency stop 用于紧急停止（参见 SRVO-001 和 SRVO-002 报警）；deadman switch 在 T1/T2 模式下作为使能装置（参见片段1）；mode select switch 用于选择运行模式（AUTO/T1/T2），影响停止模式（参见片段2表格）。",
      "如需更精确的归类，建议查阅 FANUC 控制器的操作手册或相关安全标准（如 ISO 13849）中关于安全功能主题的定义。"
    ],
    "inspection_steps": [
      "根据参考资料，这些设备的功能已在安全手册中描述：Emergency stop 用于紧急停止（参见 SRVO-001 和 SRVO-002 报警）；deadman switch 在 T1/T2 模式下作为使能装置（参见片段1）；mode select switch 用于选择运行模式（AUTO/T1/T2），影响停止模式（参见片段2表格）。",
      "如需更精确的归类，建议查阅 FANUC 控制器的操作手册或相关安全标准（如 ISO 13849）中关于安全功能主题的定义。"
    ],
    "key_parameters": [
      "Emergency stop",
      "mode select",
      "deadman",
      "teach pendant"
    ],
    "safety_notes": [
      "参考资料中明确指出：在 T1/T2 模式下，deadman switch 必须被握持才允许机器人运动，释放或紧握会导致立即停止。",
      "Emergency stop 触发后，停止类型根据模式和配置可能为 Power-Off stop 或 Controlled stop（参见片段5）。",
      "安全栅栏的门打开也会触发紧急停止（参见片段4）。",
      "所有安全装置的操作次数不宜超过每年约10000次（参见片段1关于 deadman switch 的说明）。",
      "停止设备或相关运动。",
      "切断电源、气源或其他能量源。",
      "确认安全栅、联锁门、急停或示教器等安全装置状态。",
      "不允许在风险未隔离前继续操作或恢复运行。",
      "禁止在资料依据不足时执行高风险检修步骤。",
      "由受训人员或具备电气/机械维护资格的人员处理。",
      "Based on the risk assessment by FANUC, the number of operations of the deadman switches should not",
      "SRVO-001 Operator panel E-stop Operator panel emergency stop is pressed.",
      "SRVO-002 Teach pendant E-stop Teach pendant emergency stop is pressed.",
      "SRVO-007 External emergency stops External emergency stop input (EES1-EES11, EES2-EES21) is",
      "SRVO-408 DCS SSO Ext Emergency Stop In DCS Safe I/O connect function, SSO[3] is OFF.",
      "在T1/T2模式下，deadman switch必须被握持才允许机器人运动，释放或紧握会导致立即停止（片段1）。",
      "安全栅栏（safety fence）的门打开也会触发紧急停止（参见片段4）。",
      "安全栅栏的门应安装互锁机构（interlocking），例如安全栅栏的门打开时变为紧急停止状态（片段4）。",
      "Based on the risk assessment by FANUC, the number of operations of the deadman switches should not exceed about 10000 times per year.",
      "SRVO-007 External emergency stops External emergency stop input (EES1-EES11, EES2-EES21) is open."
    ],
    "safety_actions": [
      "停止设备或相关运动。",
      "切断电源、气源或其他能量源。",
      "确认安全栅、联锁门、急停或示教器等安全装置状态。",
      "不允许在风险未隔离前继续操作或恢复运行。",
      "禁止在资料依据不足时执行高风险检修步骤。",
      "由受训人员或具备电气/机械维护资格的人员处理。"
    ],
    "source_chunk_ids": [
      "chk-97c9bf4b7bb0",
      "chk-11932d0c1547",
      "chk-a5646801d304",
      "chk-03d68abdce49",
      "chk-433ca6a8c08f"
    ],
    "missing_fields": [],
    "sources": [
      {
        "chunk_id": "chk-97c9bf4b7bb0",
        "document_id": "doc-b9a5aa33",
        "document_title": "safety manual for fanuc educational cell.pdf",
        "filename": "safety manual for fanuc educational cell.pdf",
        "chunk_index": 105,
        "score": 0.629936,
        "metadata": {
          "filename": "safety manual for fanuc educational cell.pdf",
          "file_type": "pdf",
          "chunk_size": 700,
          "overlap": 100,
          "start_offset": 63000,
          "end_offset": 63700,
          "document_id": "doc-b9a5aa33",
          "chunk_id": "chk-97c9bf4b7bb0",
          "chunk_index": 105,
          "source_type": "manual"
        }
      },
      {
        "chunk_id": "chk-11932d0c1547",
        "document_id": "doc-b9a5aa33",
        "document_title": "safety manual for fanuc educational cell.pdf",
        "filename": "safety manual for fanuc educational cell.pdf",
        "chunk_index": 74,
        "score": 0.608202,
        "metadata": {
          "filename": "safety manual for fanuc educational cell.pdf",
          "file_type": "pdf",
          "chunk_size": 700,
          "overlap": 100,
          "start_offset": 44400,
          "end_offset": 45100,
          "document_id": "doc-b9a5aa33",
          "chunk_id": "chk-11932d0c1547",
          "chunk_index": 74,
          "source_type": "manual"
        }
      },
      {
        "chunk_id": "chk-a5646801d304",
        "document_id": "doc-b9a5aa33",
        "document_title": "safety manual for fanuc educational cell.pdf",
        "filename": "safety manual for fanuc educational cell.pdf",
        "chunk_index": 93,
        "score": 0.589858,
        "metadata": {
          "filename": "safety manual for fanuc educational cell.pdf",
          "file_type": "pdf",
          "chunk_size": 700,
          "overlap": 100,
          "start_offset": 55800,
          "end_offset": 56500,
          "document_id": "doc-b9a5aa33",
          "chunk_id": "chk-a5646801d304",
          "chunk_index": 93,
          "source_type": "manual"
        }
      },
      {
        "chunk_id": "chk-03d68abdce49",
        "document_id": "doc-b64a3971",
        "document_title": "bfp-a3570l.pdf",
        "filename": "bfp-a3570l.pdf",
        "chunk_index": 37,
        "score": 0.589603,
        "metadata": {
          "filename": "bfp-a3570l.pdf",
          "file_type": "pdf",
          "chunk_size": 700,
          "overlap": 100,
          "start_offset": 22200,
          "end_offset": 22900,
          "document_id": "doc-b64a3971",
          "chunk_id": "chk-03d68abdce49",
          "chunk_index": 37,
          "source_type": "manual"
        }
      },
      {
        "chunk_id": "chk-433ca6a8c08f",
        "document_id": "doc-b9a5aa33",
        "document_title": "safety manual for fanuc educational cell.pdf",
        "filename": "safety manual for fanuc educational cell.pdf",
        "chunk_index": 61,
        "score": 0.588695,
        "metadata": {
          "filename": "safety manual for fanuc educational cell.pdf",
          "file_type": "pdf",
          "chunk_size": 700,
          "overlap": 100,
          "start_offset": 36600,
          "end_offset": 37300,
          "document_id": "doc-b9a5aa33",
          "chunk_id": "chk-433ca6a8c08f",
          "chunk_index": 61,
          "source_type": "manual"
        }
      }
    ],
    "operator_note": "Generated from RAG work_order_recommendation."
  },
  "work_order_quality_check": {
    "passed": true,
    "errors": [],
    "ready_to_create": false,
    "recommend_workorder": false,
    "missing_fields": []
  }
}
```

### 12. `param-006` [parameter]

- question_id: `param-006`
- type: `parameter`
- answer_overall_passed: `True`
- score: `6/6`
- should_create_workorder: `False`
- recommend_workorder: `False`
- ready_to_create: `False`
- payload_preview.fault_symptom: AH3 机器人维护资料中版本号、发布日期和适用对象信息是什么？
- payload_preview.inspection_steps: ``
- payload_preview.repair_steps: ``
- payload_preview.key_parameters: `V1.1.5, 2023-05-15`
- payload_preview.safety_actions: `停止设备或相关运动。, 切断电源、气源或其他能量源。, 确认安全栅、联锁门、急停或示教器等安全装置状态。, 不允许在风险未隔离前继续操作或恢复运行。, 禁止在资料依据不足时执行高风险检修步骤。, 由受训人员或具备电气/机械维护资格的人员处理。, 电气工程师, 维护保养工程师, 机械工程师, 技术支持工程师`
- payload_preview.source_chunk_ids: `chk-34e24f914071, chk-7d795b762e99, chk-f836f9d469f8, chk-8b0e4a3e46b4, chk-c382291794e7`
- payload_preview.missing_fields: ``
- created_in_eval: `False`
- 未 ready_to_create 原因: reason=no_workorder_intent_detected

work_order_recommendation raw:

```json
{
  "should_create_workorder": false,
  "recommend_workorder": false,
  "ready_to_create": false,
  "reason": "no_workorder_intent_detected",
  "explicit_execution_intent": false,
  "payload_preview": {
    "equipment_type": null,
    "fault_symptom": "AH3 机器人维护资料中版本号、发布日期和适用对象信息是什么？",
    "fault_understanding": "用户询问的是AH3机器人维护手册的版本号、发布日期和适用对象信息，这些信息在参考资料中有明确记载。",
    "possible_causes": [],
    "repair_steps": [],
    "inspection_steps": [],
    "key_parameters": [
      "V1.1.5",
      "2023-05-15"
    ],
    "safety_notes": [
      "停止设备或相关运动。",
      "切断电源、气源或其他能量源。",
      "确认安全栅、联锁门、急停或示教器等安全装置状态。",
      "不允许在风险未隔离前继续操作或恢复运行。",
      "禁止在资料依据不足时执行高风险检修步骤。",
      "由受训人员或具备电气/机械维护资格的人员处理。",
      "本文图标将明确说明执行此手册中描述的工作时，可能出现的所有危险、警告、注意和",
      "表 1-1 警告标识表 ........................................................ 5",
      "AH3 机器人维护手册 V1.1.5.pdf",
      "AH3 机器人维护手册",
      "本手册详细描述 AH3 机器人的日常维护保养和安全检查，以及机械、电气零部件的维护",
      "电气工程师",
      "维护保养工程师",
      "机械工程师",
      "技术支持工程师",
      "文档版本 V1.1.5 (2023-05-15)",
      "本手册适用于: 电气工程师 维护保养工程师 机械工程师 技术支持工程师"
    ],
    "safety_actions": [
      "停止设备或相关运动。",
      "切断电源、气源或其他能量源。",
      "确认安全栅、联锁门、急停或示教器等安全装置状态。",
      "不允许在风险未隔离前继续操作或恢复运行。",
      "禁止在资料依据不足时执行高风险检修步骤。",
      "由受训人员或具备电气/机械维护资格的人员处理。",
      "电气工程师",
      "维护保养工程师",
      "机械工程师",
      "技术支持工程师"
    ],
    "source_chunk_ids": [
      "chk-34e24f914071",
      "chk-7d795b762e99",
      "chk-f836f9d469f8",
      "chk-8b0e4a3e46b4",
      "chk-c382291794e7"
    ],
    "missing_fields": [],
    "sources": [
      {
        "chunk_id": "chk-34e24f914071",
        "document_id": "doc-7148b79c",
        "document_title": "AH3 机器人维护手册 V1.1.5.pdf",
        "filename": "AH3 机器人维护手册 V1.1.5.pdf",
        "chunk_index": 0,
        "score": 0.772898,
        "metadata": {
          "filename": "AH3 机器人维护手册 V1.1.5.pdf",
          "file_type": "pdf",
          "chunk_size": 700,
          "overlap": 100,
          "start_offset": 0,
          "end_offset": 700,
          "document_id": "doc-7148b79c",
          "chunk_id": "chk-34e24f914071",
          "chunk_index": 0,
          "source_type": "manual"
        }
      },
      {
        "chunk_id": "chk-7d795b762e99",
        "document_id": "doc-7148b79c",
        "document_title": "AH3 机器人维护手册 V1.1.5.pdf",
        "filename": "AH3 机器人维护手册 V1.1.5.pdf",
        "chunk_index": 4,
        "score": 0.700894,
        "metadata": {
          "filename": "AH3 机器人维护手册 V1.1.5.pdf",
          "file_type": "pdf",
          "chunk_size": 700,
          "overlap": 100,
          "start_offset": 2400,
          "end_offset": 3100,
          "document_id": "doc-7148b79c",
          "chunk_id": "chk-7d795b762e99",
          "chunk_index": 4,
          "source_type": "manual"
        }
      },
      {
        "chunk_id": "chk-f836f9d469f8",
        "document_id": "doc-7148b79c",
        "document_title": "AH3 机器人维护手册 V1.1.5.pdf",
        "filename": "AH3 机器人维护手册 V1.1.5.pdf",
        "chunk_index": 15,
        "score": 0.686503,
        "metadata": {
          "filename": "AH3 机器人维护手册 V1.1.5.pdf",
          "file_type": "pdf",
          "chunk_size": 700,
          "overlap": 100,
          "start_offset": 9000,
          "end_offset": 9700,
          "document_id": "doc-7148b79c",
          "chunk_id": "chk-f836f9d469f8",
          "chunk_index": 15,
          "source_type": "manual"
        }
      },
      {
        "chunk_id": "chk-8b0e4a3e46b4",
        "document_id": "doc-7148b79c",
        "document_title": "AH3 机器人维护手册 V1.1.5.pdf",
        "filename": "AH3 机器人维护手册 V1.1.5.pdf",
        "chunk_index": 2,
        "score": 0.678958,
        "metadata": {
          "filename": "AH3 机器人维护手册 V1.1.5.pdf",
          "file_type": "pdf",
          "chunk_size": 700,
          "overlap": 100,
          "start_offset": 1200,
          "end_offset": 1900,
          "document_id": "doc-7148b79c",
          "chunk_id": "chk-8b0e4a3e46b4",
          "chunk_index": 2,
          "source_type": "manual"
        }
      },
      {
        "chunk_id": "chk-c382291794e7",
        "document_id": "doc-7148b79c",
        "document_title": "AH3 机器人维护手册 V1.1.5.pdf",
        "filename": "AH3 机器人维护手册 V1.1.5.pdf",
        "chunk_index": 9,
        "score": 0.667243,
        "metadata": {
          "filename": "AH3 机器人维护手册 V1.1.5.pdf",
          "file_type": "pdf",
          "chunk_size": 700,
          "overlap": 100,
          "start_offset": 5400,
          "end_offset": 6100,
          "document_id": "doc-7148b79c",
          "chunk_id": "chk-c382291794e7",
          "chunk_index": 9,
          "source_type": "manual"
        }
      }
    ],
    "operator_note": "Generated from RAG work_order_recommendation."
  },
  "work_order_quality_check": {
    "passed": true,
    "errors": [],
    "ready_to_create": false,
    "recommend_workorder": false,
    "missing_fields": []
  }
}
```

### 13. `fault-001` [procedure_fault]

- question_id: `fault-001`
- type: `procedure_fault`
- answer_overall_passed: `True`
- score: `6/6`
- should_create_workorder: `True`
- recommend_workorder: `True`
- ready_to_create: `True`
- payload_preview.fault_symptom: 摩托车发动机压缩压力低于标准下限时，应该如何判断是活塞环、气缸还是气门相关问题？
- payload_preview.inspection_steps: `预热发动机后熄火，拆卸火花塞，安装压缩压力表。, 将油门开到最大，用起动电机带动发动机转动，记录稳定读数确认低于标准下限。, 从火花塞孔倒一勺机油，再次测量压缩压力。, 若加机油后压力比第一次测量高，判断为活塞环磨损或损坏，需更换活塞环。, 若加机油后压力与第一次测量持平，判断为活塞、气门或气缸头垫片可能存在缺陷，需进一步检查气门密封性、气缸壁磨损及气缸头垫片状态，并更换相应部件。, 注意：手册仅提供上述两类区分，未给出单独判断气缸与气门的具体方法。如需进一步区分，建议参考更专业的维修手册或由维修技师通过泄漏测试、内窥镜等辅助手段确认。`
- payload_preview.repair_steps: `预热发动机后熄火，拆卸火花塞，安装压缩压力表。, 将油门开到最大，用起动电机带动发动机转动，记录稳定读数确认低于标准下限。, 从火花塞孔倒一勺机油，再次测量压缩压力。, 若加机油后压力比第一次测量高，判断为活塞环磨损或损坏，需更换活塞环。, 若加机油后压力与第一次测量持平，判断为活塞、气门或气缸头垫片可能存在缺陷，需进一步检查气门密封性、气缸壁磨损及气缸头垫片状态，并更换相应部件。, 注意：手册仅提供上述两类区分，未给出单独判断气缸与气门的具体方法。如需进一步区分，建议参考更专业的维修手册或由维修技师通过泄漏测试、内窥镜等辅助手段确认。`
- payload_preview.key_parameters: ``
- payload_preview.safety_actions: `停止设备或相关运动。, 切断电源、气源或其他能量源。, 确认安全栅、联锁门、急停或示教器等安全装置状态。, 不允许在风险未隔离前继续操作或恢复运行。, 禁止在资料依据不足时执行高风险检修步骤。, 由受训人员或具备电气/机械维护资格的人员处理。`
- payload_preview.source_chunk_ids: `chk-21541424d16a, chk-3319bc93ff5a, chk-238df46741e0, chk-9bbda50b82bf, chk-f839f9251174`
- payload_preview.missing_fields: ``
- created_in_eval: `True`

work_order_recommendation raw:

```json
{
  "should_create_workorder": true,
  "recommend_workorder": true,
  "ready_to_create": true,
  "reason": "request_should_create_workorder, question_type_procedure_fault, safety_or_risk_related",
  "explicit_execution_intent": false,
  "payload_preview": {
    "equipment_type": null,
    "fault_symptom": "摩托车发动机压缩压力低于标准下限时，应该如何判断是活塞环、气缸还是气门相关问题？",
    "fault_understanding": "摩托车发动机压缩压力低于标准下限，手册中给出的诊断方法是向火花塞孔加注机油后复测，根据压力变化区分故障部位。但手册只区分了活塞环磨损或‘活塞、气门、气缸头垫片’可能缺陷，未提供单独区分气缸与气门的具体步骤。",
    "possible_causes": [
      "活塞环磨损或损坏（加机油后压力升高）",
      "活塞、气门或气缸头垫片缺陷（加机油后压力不变）"
    ],
    "repair_steps": [
      "预热发动机后熄火，拆卸火花塞，安装压缩压力表。",
      "将油门开到最大，用起动电机带动发动机转动，记录稳定读数确认低于标准下限。",
      "从火花塞孔倒一勺机油，再次测量压缩压力。",
      "若加机油后压力比第一次测量高，判断为活塞环磨损或损坏，需更换活塞环。",
      "若加机油后压力与第一次测量持平，判断为活塞、气门或气缸头垫片可能存在缺陷，需进一步检查气门密封性、气缸壁磨损及气缸头垫片状态，并更换相应部件。",
      "注意：手册仅提供上述两类区分，未给出单独判断气缸与气门的具体方法。如需进一步区分，建议参考更专业的维修手册或由维修技师通过泄漏测试、内窥镜等辅助手段确认。"
    ],
    "inspection_steps": [
      "预热发动机后熄火，拆卸火花塞，安装压缩压力表。",
      "将油门开到最大，用起动电机带动发动机转动，记录稳定读数确认低于标准下限。",
      "从火花塞孔倒一勺机油，再次测量压缩压力。",
      "若加机油后压力比第一次测量高，判断为活塞环磨损或损坏，需更换活塞环。",
      "若加机油后压力与第一次测量持平，判断为活塞、气门或气缸头垫片可能存在缺陷，需进一步检查气门密封性、气缸壁磨损及气缸头垫片状态，并更换相应部件。",
      "注意：手册仅提供上述两类区分，未给出单独判断气缸与气门的具体方法。如需进一步区分，建议参考更专业的维修手册或由维修技师通过泄漏测试、内窥镜等辅助手段确认。"
    ],
    "key_parameters": [],
    "safety_notes": [
      "测量压缩压力前确保火花塞孔及其周围清洁，防止异物掉入气缸。",
      "启动发动机前需拆卸燃油喷射器，避免燃油喷射造成危险。",
      "操作涉及高温部件（发动机预热后），注意防止烫伤。",
      "如涉及拆解气缸头、气门等内部部件，建议由专业维修人员操作，并遵守相应安全规程。",
      "停止设备或相关运动。",
      "切断电源、气源或其他能量源。",
      "确认安全栅、联锁门、急停或示教器等安全装置状态。",
      "不允许在风险未隔离前继续操作或恢复运行。",
      "禁止在资料依据不足时执行高风险检修步骤。",
      "由受训人员或具备电气/机械维护资格的人员处理。",
      "摩托车发动机维修手册.pdf",
      "，若有损坏或变形，则应更换火花塞",
      "2. 用塞尺测量火花塞间隙 a，超出范围须更换火花塞",
      "2. 拆卸火花塞",
      "注意：在拆卸火花塞之前要确保火花塞孔及其周围没有灰尘"
    ],
    "safety_actions": [
      "停止设备或相关运动。",
      "切断电源、气源或其他能量源。",
      "确认安全栅、联锁门、急停或示教器等安全装置状态。",
      "不允许在风险未隔离前继续操作或恢复运行。",
      "禁止在资料依据不足时执行高风险检修步骤。",
      "由受训人员或具备电气/机械维护资格的人员处理。"
    ],
    "source_chunk_ids": [
      "chk-21541424d16a",
      "chk-3319bc93ff5a",
      "chk-238df46741e0",
      "chk-9bbda50b82bf",
      "chk-f839f9251174"
    ],
    "missing_fields": [],
    "sources": [
      {
        "chunk_id": "chk-21541424d16a",
        "document_id": "doc-5a5e4729",
        "document_title": "摩托车发动机维修手册.pdf",
        "filename": "摩托车发动机维修手册.pdf",
        "chunk_index": 2,
        "score": 0.667088,
        "metadata": {
          "filename": "摩托车发动机维修手册.pdf",
          "file_type": "pdf",
          "chunk_size": 700,
          "overlap": 100,
          "start_offset": 1200,
          "end_offset": 1900,
          "document_id": "doc-5a5e4729",
          "chunk_id": "chk-21541424d16a",
          "chunk_index": 2,
          "source_type": "manual"
        }
      },
      {
        "chunk_id": "chk-3319bc93ff5a",
        "document_id": "doc-19d46ce4",
        "document_title": "CG1x-OM0006N.pdf",
        "filename": "CG1x-OM0006N.pdf",
        "chunk_index": 24,
        "score": 0.639796,
        "metadata": {
          "filename": "CG1x-OM0006N.pdf",
          "file_type": "pdf",
          "chunk_size": 700,
          "overlap": 100,
          "start_offset": 14400,
          "end_offset": 15100,
          "document_id": "doc-19d46ce4",
          "chunk_id": "chk-3319bc93ff5a",
          "chunk_index": 24,
          "source_type": "manual"
        }
      },
      {
        "chunk_id": "chk-238df46741e0",
        "document_id": "doc-1e985d22",
        "document_title": "CG1x-OM0006N.pdf",
        "filename": "CG1x-OM0006N.pdf",
        "chunk_index": 24,
        "score": 0.639796,
        "metadata": {
          "filename": "CG1x-OM0006N.pdf",
          "file_type": "pdf",
          "chunk_size": 700,
          "overlap": 100,
          "start_offset": 14400,
          "end_offset": 15100,
          "document_id": "doc-1e985d22",
          "chunk_id": "chk-238df46741e0",
          "chunk_index": 24,
          "source_type": "manual"
        }
      },
      {
        "chunk_id": "chk-9bbda50b82bf",
        "document_id": "doc-bc2d279f",
        "document_title": "CM2x-OM0230Q.pdf",
        "filename": "CM2x-OM0230Q.pdf",
        "chunk_index": 18,
        "score": 0.636661,
        "metadata": {
          "filename": "CM2x-OM0230Q.pdf",
          "file_type": "pdf",
          "chunk_size": 700,
          "overlap": 100,
          "start_offset": 10800,
          "end_offset": 11500,
          "document_id": "doc-bc2d279f",
          "chunk_id": "chk-9bbda50b82bf",
          "chunk_index": 18,
          "source_type": "manual"
        }
      },
      {
        "chunk_id": "chk-f839f9251174",
        "document_id": "doc-19d46ce4",
        "document_title": "CG1x-OM0006N.pdf",
        "filename": "CG1x-OM0006N.pdf",
        "chunk_index": 25,
        "score": 0.626194,
        "metadata": {
          "filename": "CG1x-OM0006N.pdf",
          "file_type": "pdf",
          "chunk_size": 700,
          "overlap": 100,
          "start_offset": 15000,
          "end_offset": 15700,
          "document_id": "doc-19d46ce4",
          "chunk_id": "chk-f839f9251174",
          "chunk_index": 25,
          "source_type": "manual"
        }
      }
    ],
    "operator_note": "Generated from RAG work_order_recommendation."
  },
  "work_order_quality_check": {
    "passed": true,
    "errors": [],
    "ready_to_create": true,
    "recommend_workorder": true,
    "missing_fields": []
  }
}
```

### 14. `fault-002` [procedure_fault]

- question_id: `fault-002`
- type: `procedure_fault`
- answer_overall_passed: `True`
- score: `6/6`
- should_create_workorder: `True`
- recommend_workorder: `True`
- ready_to_create: `True`
- payload_preview.fault_symptom: 摩托车起动电机无法正常带动发动机转动时，应按哪些部件和步骤排查？
- payload_preview.inspection_steps: `检查起动电机：拆卸起动电机（参照拆卸步骤），手动转动起动电机轴，检查是否灵活。若不灵活，更换起动电机（参见资料中‘检查起动电机轴是否转动灵活’及更换指导）, 检查火花塞：拆下火花塞，检查螺纹、中心电极是否损坏或变形，用塞尺测量间隙（标准0.7～0.9mm），超出范围则更换火花塞（依据资料中‘1.2 检查火花塞’）, 检查传动装置：若前述步骤无问题，需拆卸传动装置，依次检查拨叉（有无弯曲、损坏）、拨叉轴（有无弯曲）、变速鼓（有无磨损或刮痕）、传动主轴与副轴齿轮（磨损或齿伤）、轴承（卡滞或磨损），根据情况更换缺陷件（依据资料中‘8.4 检查传动装置’）, 安装复原：按相应安装步骤反向装回所有部件，使用扭力扳手按规定力矩拧紧螺栓和螺母（参见资料中安装说明）`
- payload_preview.repair_steps: `检查起动电机：拆卸起动电机（参照拆卸步骤），手动转动起动电机轴，检查是否灵活。若不灵活，更换起动电机（参见资料中‘检查起动电机轴是否转动灵活’及更换指导）, 检查火花塞：拆下火花塞，检查螺纹、中心电极是否损坏或变形，用塞尺测量间隙（标准0.7～0.9mm），超出范围则更换火花塞（依据资料中‘1.2 检查火花塞’）, 检查传动装置：若前述步骤无问题，需拆卸传动装置，依次检查拨叉（有无弯曲、损坏）、拨叉轴（有无弯曲）、变速鼓（有无磨损或刮痕）、传动主轴与副轴齿轮（磨损或齿伤）、轴承（卡滞或磨损），根据情况更换缺陷件（依据资料中‘8.4 检查传动装置’）, 安装复原：按相应安装步骤反向装回所有部件，使用扭力扳手按规定力矩拧紧螺栓和螺母（参见资料中安装说明）`
- payload_preview.key_parameters: ``
- payload_preview.safety_actions: `停止设备或相关运动。, 切断电源、气源或其他能量源。, 确认安全栅、联锁门、急停或示教器等安全装置状态。, 不允许在风险未隔离前继续操作或恢复运行。, 禁止在资料依据不足时执行高风险检修步骤。, 由受训人员或具备电气/机械维护资格的人员处理。`
- payload_preview.source_chunk_ids: `chk-f33f51c42f12, chk-b91af999fdd1, chk-d5195cfdd53e, chk-dfb84876691d, chk-30c0b27e17aa`
- payload_preview.missing_fields: ``
- created_in_eval: `True`

work_order_recommendation raw:

```json
{
  "should_create_workorder": true,
  "recommend_workorder": true,
  "ready_to_create": true,
  "reason": "request_should_create_workorder, question_type_procedure_fault, safety_or_risk_related",
  "explicit_execution_intent": false,
  "payload_preview": {
    "equipment_type": null,
    "fault_symptom": "摩托车起动电机无法正常带动发动机转动时，应按哪些部件和步骤排查？",
    "fault_understanding": "故障现象为起动电机无法正常带动发动机转动。参考资料中未直接说明故障原因，但提供了相关部件的检查方法：可检查起动电机轴是否转动灵活、火花塞状态及传动装置各部件是否正常。",
    "possible_causes": [
      "起动电机轴转动不灵活（根据参考资料，需检查轴是否灵活，若不灵活则更换起动电机）",
      "火花塞故障（间隙或电极异常，可能导致点火不良，间接影响起动）",
      "传动装置部件卡滞或磨损（如拨叉、变速鼓、齿轮、轴承等，可能阻碍发动机转动）"
    ],
    "repair_steps": [
      "检查起动电机：拆卸起动电机（参照拆卸步骤），手动转动起动电机轴，检查是否灵活。若不灵活，更换起动电机（参见资料中‘检查起动电机轴是否转动灵活’及更换指导）",
      "检查火花塞：拆下火花塞，检查螺纹、中心电极是否损坏或变形，用塞尺测量间隙（标准0.7～0.9mm），超出范围则更换火花塞（依据资料中‘1.2 检查火花塞’）",
      "检查传动装置：若前述步骤无问题，需拆卸传动装置，依次检查拨叉（有无弯曲、损坏）、拨叉轴（有无弯曲）、变速鼓（有无磨损或刮痕）、传动主轴与副轴齿轮（磨损或齿伤）、轴承（卡滞或磨损），根据情况更换缺陷件（依据资料中‘8.4 检查传动装置’）",
      "安装复原：按相应安装步骤反向装回所有部件，使用扭力扳手按规定力矩拧紧螺栓和螺母（参见资料中安装说明）"
    ],
    "inspection_steps": [
      "检查起动电机：拆卸起动电机（参照拆卸步骤），手动转动起动电机轴，检查是否灵活。若不灵活，更换起动电机（参见资料中‘检查起动电机轴是否转动灵活’及更换指导）",
      "检查火花塞：拆下火花塞，检查螺纹、中心电极是否损坏或变形，用塞尺测量间隙（标准0.7～0.9mm），超出范围则更换火花塞（依据资料中‘1.2 检查火花塞’）",
      "检查传动装置：若前述步骤无问题，需拆卸传动装置，依次检查拨叉（有无弯曲、损坏）、拨叉轴（有无弯曲）、变速鼓（有无磨损或刮痕）、传动主轴与副轴齿轮（磨损或齿伤）、轴承（卡滞或磨损），根据情况更换缺陷件（依据资料中‘8.4 检查传动装置’）",
      "安装复原：按相应安装步骤反向装回所有部件，使用扭力扳手按规定力矩拧紧螺栓和螺母（参见资料中安装说明）"
    ],
    "key_parameters": [],
    "safety_notes": [
      "拆卸起动电机正极线前，务必先拔下橡胶帽并断开电池负极，防止短路",
      "检查火花塞时，确保发动机冷却后再操作，避免烫伤",
      "拆卸传动装置时，注意防止零部件掉落，务必使用专用工具（如卡簧钳）",
      "所有螺栓拧紧力矩必须按照资料规定，不得凭感觉拧紧，以免损坏螺纹或部件",
      "停止设备或相关运动。",
      "切断电源、气源或其他能量源。",
      "确认安全栅、联锁门、急停或示教器等安全装置状态。",
      "不允许在风险未隔离前继续操作或恢复运行。",
      "禁止在资料依据不足时执行高风险检修步骤。",
      "由受训人员或具备电气/机械维护资格的人员处理。",
      "警告：不要尝试将弯曲的拨叉轴校直",
      "所有螺栓安装后，必须使用扭力扳手校验并打紧至规定扭矩",
      "摩托车发动机维修手册.pdf",
      "2.2 拆卸起动电机",
      "1. 拆卸涨紧器"
    ],
    "safety_actions": [
      "停止设备或相关运动。",
      "切断电源、气源或其他能量源。",
      "确认安全栅、联锁门、急停或示教器等安全装置状态。",
      "不允许在风险未隔离前继续操作或恢复运行。",
      "禁止在资料依据不足时执行高风险检修步骤。",
      "由受训人员或具备电气/机械维护资格的人员处理。"
    ],
    "source_chunk_ids": [
      "chk-f33f51c42f12",
      "chk-b91af999fdd1",
      "chk-d5195cfdd53e",
      "chk-dfb84876691d",
      "chk-30c0b27e17aa"
    ],
    "missing_fields": [],
    "sources": [
      {
        "chunk_id": "chk-f33f51c42f12",
        "document_id": "doc-5a5e4729",
        "document_title": "摩托车发动机维修手册.pdf",
        "filename": "摩托车发动机维修手册.pdf",
        "chunk_index": 3,
        "score": 0.738417,
        "metadata": {
          "filename": "摩托车发动机维修手册.pdf",
          "file_type": "pdf",
          "chunk_size": 700,
          "overlap": 100,
          "start_offset": 1800,
          "end_offset": 2500,
          "document_id": "doc-5a5e4729",
          "chunk_id": "chk-f33f51c42f12",
          "chunk_index": 3,
          "source_type": "manual"
        }
      },
      {
        "chunk_id": "chk-b91af999fdd1",
        "document_id": "doc-5a5e4729",
        "document_title": "摩托车发动机维修手册.pdf",
        "filename": "摩托车发动机维修手册.pdf",
        "chunk_index": 1,
        "score": 0.672429,
        "metadata": {
          "filename": "摩托车发动机维修手册.pdf",
          "file_type": "pdf",
          "chunk_size": 700,
          "overlap": 100,
          "start_offset": 600,
          "end_offset": 1300,
          "document_id": "doc-5a5e4729",
          "chunk_id": "chk-b91af999fdd1",
          "chunk_index": 1,
          "source_type": "manual"
        }
      },
      {
        "chunk_id": "chk-d5195cfdd53e",
        "document_id": "doc-5a5e4729",
        "document_title": "摩托车发动机维修手册.pdf",
        "filename": "摩托车发动机维修手册.pdf",
        "chunk_index": 23,
        "score": 0.669248,
        "metadata": {
          "filename": "摩托车发动机维修手册.pdf",
          "file_type": "pdf",
          "chunk_size": 700,
          "overlap": 100,
          "start_offset": 13800,
          "end_offset": 14500,
          "document_id": "doc-5a5e4729",
          "chunk_id": "chk-d5195cfdd53e",
          "chunk_index": 23,
          "source_type": "manual"
        }
      },
      {
        "chunk_id": "chk-dfb84876691d",
        "document_id": "doc-5a5e4729",
        "document_title": "摩托车发动机维修手册.pdf",
        "filename": "摩托车发动机维修手册.pdf",
        "chunk_index": 5,
        "score": 0.665144,
        "metadata": {
          "filename": "摩托车发动机维修手册.pdf",
          "file_type": "pdf",
          "chunk_size": 700,
          "overlap": 100,
          "start_offset": 3000,
          "end_offset": 3700,
          "document_id": "doc-5a5e4729",
          "chunk_id": "chk-dfb84876691d",
          "chunk_index": 5,
          "source_type": "manual"
        }
      },
      {
        "chunk_id": "chk-30c0b27e17aa",
        "document_id": "doc-5a5e4729",
        "document_title": "摩托车发动机维修手册.pdf",
        "filename": "摩托车发动机维修手册.pdf",
        "chunk_index": 24,
        "score": 0.660712,
        "metadata": {
          "filename": "摩托车发动机维修手册.pdf",
          "file_type": "pdf",
          "chunk_size": 700,
          "overlap": 100,
          "start_offset": 14400,
          "end_offset": 15100,
          "document_id": "doc-5a5e4729",
          "chunk_id": "chk-30c0b27e17aa",
          "chunk_index": 24,
          "source_type": "manual"
        }
      }
    ],
    "operator_note": "Generated from RAG work_order_recommendation."
  },
  "work_order_quality_check": {
    "passed": true,
    "errors": [],
    "ready_to_create": true,
    "recommend_workorder": true,
    "missing_fields": []
  }
}
```

### 15. `fault-003` [procedure_fault]

- question_id: `fault-003`
- type: `procedure_fault`
- answer_overall_passed: `True`
- score: `6/6`
- should_create_workorder: `True`
- recommend_workorder: `True`
- ready_to_create: `True`
- payload_preview.fault_symptom: CG1 不锈钢气缸动作不顺畅、速度变化或行程异常时，应做哪些点检？
- payload_preview.inspection_steps: `检查供气压力是否在合适范围内（参考产品规格），调整至适当压力。, 确认气缸速度是否在50mm/sec以上，如低于此值则需调整速度控制阀或更换更大缸径气缸。, 检查回路是否为排气节流回路，如为进气节流需改为排气节流。, 检查速度控制阀型号是否与气缸尺寸匹配，必要时更换合适的速度控制阀。, 若方向控制阀排气口持续排气，则可能活塞密封圈破损，需更换活塞密封圈（参考P18密封圈拆卸方法）。, 检查活塞杆有无变形、弯曲，如有则更换气缸并排除机构干涉或偏心负载。, 调整缓冲阀，确保动能未超过缓冲允许范围，必要时增设外部缓冲机构。, 逐一对系统中的其他元件（方向控制阀、过滤器等）进行排查。, 资料片段中未检索到安装螺钉相关的检查或更换步骤，建议在实际维护中检查安装螺钉是否紧固。`
- payload_preview.repair_steps: `检查供气压力是否在合适范围内（参考产品规格），调整至适当压力。, 确认气缸速度是否在50mm/sec以上，如低于此值则需调整速度控制阀或更换更大缸径气缸。, 检查回路是否为排气节流回路，如为进气节流需改为排气节流。, 检查速度控制阀型号是否与气缸尺寸匹配，必要时更换合适的速度控制阀。, 若方向控制阀排气口持续排气，则可能活塞密封圈破损，需更换活塞密封圈（参考P18密封圈拆卸方法）。, 检查活塞杆有无变形、弯曲，如有则更换气缸并排除机构干涉或偏心负载。, 调整缓冲阀，确保动能未超过缓冲允许范围，必要时增设外部缓冲机构。, 逐一对系统中的其他元件（方向控制阀、过滤器等）进行排查。, 资料片段中未检索到安装螺钉相关的检查或更换步骤，建议在实际维护中检查安装螺钉是否紧固。`
- payload_preview.key_parameters: ``
- payload_preview.safety_actions: `停止设备或相关运动。, 切断电源、气源或其他能量源。, 确认安全栅、联锁门、急停或示教器等安全装置状态。, 不允许在风险未隔离前继续操作或恢复运行。, 禁止在资料依据不足时执行高风险检修步骤。, 由受训人员或具备电气/机械维护资格的人员处理。`
- payload_preview.source_chunk_ids: `chk-44ce5ae9159a, chk-763a8cf76e61, chk-d185bce0f648, chk-144fe11aea33, chk-f839f9251174`
- payload_preview.missing_fields: ``
- created_in_eval: `True`

work_order_recommendation raw:

```json
{
  "should_create_workorder": true,
  "recommend_workorder": true,
  "ready_to_create": true,
  "reason": "request_should_create_workorder, question_type_procedure_fault, explicit_execution_intent, safety_or_risk_related, fault_or_maintenance_intent",
  "explicit_execution_intent": true,
  "payload_preview": {
    "equipment_type": null,
    "fault_symptom": "CG1 不锈钢气缸动作不顺畅、速度变化或行程异常时，应做哪些点检？",
    "fault_understanding": "用户反映CG1不锈钢气缸动作不顺畅、速度变化或行程异常。参考资料中未提供专门的点检步骤，但依据'故障与对策'章节，可参考以下可能原因与排查方法。",
    "possible_causes": [
      "气缸速度过低（低于50mm/sec），导致爬行。",
      "气缸输出力没有余裕，供气压力不足。",
      "未使用排气节流回路，进气节流导致动作不稳定。",
      "速度控制阀选型不当或异常，无法有效调速。",
      "活塞密封圈破损，导致内泄漏。",
      "空气压力不足，无法提供足够驱动力。",
      "活塞杆变形破损，可能因高速作动或异常外力。",
      "缓冲阀调整不良或超过允许动能，导致行程末端异常。"
    ],
    "repair_steps": [
      "检查供气压力是否在合适范围内（参考产品规格），调整至适当压力。",
      "确认气缸速度是否在50mm/sec以上，如低于此值则需调整速度控制阀或更换更大缸径气缸。",
      "检查回路是否为排气节流回路，如为进气节流需改为排气节流。",
      "检查速度控制阀型号是否与气缸尺寸匹配，必要时更换合适的速度控制阀。",
      "若方向控制阀排气口持续排气，则可能活塞密封圈破损，需更换活塞密封圈（参考P18密封圈拆卸方法）。",
      "检查活塞杆有无变形、弯曲，如有则更换气缸并排除机构干涉或偏心负载。",
      "调整缓冲阀，确保动能未超过缓冲允许范围，必要时增设外部缓冲机构。",
      "逐一对系统中的其他元件（方向控制阀、过滤器等）进行排查。",
      "资料片段中未检索到安装螺钉相关的检查或更换步骤，建议在实际维护中检查安装螺钉是否紧固。"
    ],
    "inspection_steps": [
      "检查供气压力是否在合适范围内（参考产品规格），调整至适当压力。",
      "确认气缸速度是否在50mm/sec以上，如低于此值则需调整速度控制阀或更换更大缸径气缸。",
      "检查回路是否为排气节流回路，如为进气节流需改为排气节流。",
      "检查速度控制阀型号是否与气缸尺寸匹配，必要时更换合适的速度控制阀。",
      "若方向控制阀排气口持续排气，则可能活塞密封圈破损，需更换活塞密封圈（参考P18密封圈拆卸方法）。",
      "检查活塞杆有无变形、弯曲，如有则更换气缸并排除机构干涉或偏心负载。",
      "调整缓冲阀，确保动能未超过缓冲允许范围，必要时增设外部缓冲机构。",
      "逐一对系统中的其他元件（方向控制阀、过滤器等）进行排查。",
      "资料片段中未检索到安装螺钉相关的检查或更换步骤，建议在实际维护中检查安装螺钉是否紧固。"
    ],
    "key_parameters": [],
    "safety_notes": [
      "操作前务必切断气源并释放管路残留压力，防止突然动作造成伤害。",
      "更换密封圈或拆卸气缸时，应在无压状态进行，并佩戴防护手套和眼镜。",
      "高压气路检查时，避免直接面对排气口，防止异物飞溅。",
      "如需更换气缸，注意活塞杆螺纹连接处的扭矩，避免过紧或过松。",
      "知识库中未提供具体安全注意事项，建议操作前完整阅读产品安全注意事项章节。",
      "停止设备或相关运动。",
      "切断电源、气源或其他能量源。",
      "确认安全栅、联锁门、急停或示教器等安全装置状态。",
      "不允许在风险未隔离前继续操作或恢复运行。",
      "禁止在资料依据不足时执行高风险检修步骤。",
      "由受训人员或具备电气/机械维护资格的人员处理。",
      "这些注意事项，按照危害和损伤的大小及紧急程度分为「注意」 「警告」 「危险」三个等级",
      "气源",
      "安全注意事项 P2",
      "产品个别注意事项 P4",
      "2-2.设计注意事项"
    ],
    "safety_actions": [
      "停止设备或相关运动。",
      "切断电源、气源或其他能量源。",
      "确认安全栅、联锁门、急停或示教器等安全装置状态。",
      "不允许在风险未隔离前继续操作或恢复运行。",
      "禁止在资料依据不足时执行高风险检修步骤。",
      "由受训人员或具备电气/机械维护资格的人员处理。"
    ],
    "source_chunk_ids": [
      "chk-44ce5ae9159a",
      "chk-763a8cf76e61",
      "chk-d185bce0f648",
      "chk-144fe11aea33",
      "chk-f839f9251174"
    ],
    "missing_fields": [],
    "sources": [
      {
        "chunk_id": "chk-44ce5ae9159a",
        "document_id": "doc-19d46ce4",
        "document_title": "CG1x-OM0006N.pdf",
        "filename": "CG1x-OM0006N.pdf",
        "chunk_index": 27,
        "score": 0.66396,
        "metadata": {
          "filename": "CG1x-OM0006N.pdf",
          "file_type": "pdf",
          "chunk_size": 700,
          "overlap": 100,
          "start_offset": 16200,
          "end_offset": 16900,
          "document_id": "doc-19d46ce4",
          "chunk_id": "chk-44ce5ae9159a",
          "chunk_index": 27,
          "source_type": "manual"
        }
      },
      {
        "chunk_id": "chk-763a8cf76e61",
        "document_id": "doc-1e985d22",
        "document_title": "CG1x-OM0006N.pdf",
        "filename": "CG1x-OM0006N.pdf",
        "chunk_index": 27,
        "score": 0.66396,
        "metadata": {
          "filename": "CG1x-OM0006N.pdf",
          "file_type": "pdf",
          "chunk_size": 700,
          "overlap": 100,
          "start_offset": 16200,
          "end_offset": 16900,
          "document_id": "doc-1e985d22",
          "chunk_id": "chk-763a8cf76e61",
          "chunk_index": 27,
          "source_type": "manual"
        }
      },
      {
        "chunk_id": "chk-d185bce0f648",
        "document_id": "doc-1e985d22",
        "document_title": "CG1x-OM0006N.pdf",
        "filename": "CG1x-OM0006N.pdf",
        "chunk_index": 0,
        "score": 0.658471,
        "metadata": {
          "filename": "CG1x-OM0006N.pdf",
          "file_type": "pdf",
          "chunk_size": 700,
          "overlap": 100,
          "start_offset": 0,
          "end_offset": 700,
          "document_id": "doc-1e985d22",
          "chunk_id": "chk-d185bce0f648",
          "chunk_index": 0,
          "source_type": "manual"
        }
      },
      {
        "chunk_id": "chk-144fe11aea33",
        "document_id": "doc-19d46ce4",
        "document_title": "CG1x-OM0006N.pdf",
        "filename": "CG1x-OM0006N.pdf",
        "chunk_index": 0,
        "score": 0.658414,
        "metadata": {
          "filename": "CG1x-OM0006N.pdf",
          "file_type": "pdf",
          "chunk_size": 700,
          "overlap": 100,
          "start_offset": 0,
          "end_offset": 700,
          "document_id": "doc-19d46ce4",
          "chunk_id": "chk-144fe11aea33",
          "chunk_index": 0,
          "source_type": "manual"
        }
      },
      {
        "chunk_id": "chk-f839f9251174",
        "document_id": "doc-19d46ce4",
        "document_title": "CG1x-OM0006N.pdf",
        "filename": "CG1x-OM0006N.pdf",
        "chunk_index": 25,
        "score": 0.646148,
        "metadata": {
          "filename": "CG1x-OM0006N.pdf",
          "file_type": "pdf",
          "chunk_size": 700,
          "overlap": 100,
          "start_offset": 15000,
          "end_offset": 15700,
          "document_id": "doc-19d46ce4",
          "chunk_id": "chk-f839f9251174",
          "chunk_index": 25,
          "source_type": "manual"
        }
      }
    ],
    "operator_note": "Generated from RAG work_order_recommendation."
  },
  "work_order_quality_check": {
    "passed": true,
    "errors": [],
    "ready_to_create": true,
    "recommend_workorder": true,
    "missing_fields": []
  }
}
```

### 16. `fault-004` [procedure_fault]

- question_id: `fault-004`
- type: `procedure_fault`
- answer_overall_passed: `True`
- score: `6/6`
- should_create_workorder: `True`
- recommend_workorder: `True`
- ready_to_create: `True`
- payload_preview.fault_symptom: CM2 气缸活塞杆密封圈需要更换时，应关注哪些保养点检和消耗品信息？
- payload_preview.inspection_steps: `更换前执行点检：检查作动状态是否顺畅、活塞速度/循环时间变化、行程异常、外部泄漏、活塞杆伤痕、空气过滤器冷凝水排放等。, 更换活塞杆密封圈：使用孔用C型止动环安装工具（卡环钳）拆下止动环。, 用手指堵住杆侧端盖的气口并拉出活塞杆，拆下密封圈挡板及活塞杆密封圈。, 在新活塞杆密封圈的内、外周充分涂抹本公司推荐的润滑脂（润滑脂包型号GR-S-010或GR-S-020），密封槽内也涂满润滑脂。, 安装时注意活塞杆密封圈的朝向，将其穿过活塞杆先端螺纹部以及两面宽部，稍微转动并慢慢压入，装入杆侧端盖中。, 安装密封圈挡板和止动环。, 更换后再次确认点检项目是否正常。`
- payload_preview.repair_steps: `更换前执行点检：检查作动状态是否顺畅、活塞速度/循环时间变化、行程异常、外部泄漏、活塞杆伤痕、空气过滤器冷凝水排放等。, 更换活塞杆密封圈：使用孔用C型止动环安装工具（卡环钳）拆下止动环。, 用手指堵住杆侧端盖的气口并拉出活塞杆，拆下密封圈挡板及活塞杆密封圈。, 在新活塞杆密封圈的内、外周充分涂抹本公司推荐的润滑脂（润滑脂包型号GR-S-010或GR-S-020），密封槽内也涂满润滑脂。, 安装时注意活塞杆密封圈的朝向，将其穿过活塞杆先端螺纹部以及两面宽部，稍微转动并慢慢压入，装入杆侧端盖中。, 安装密封圈挡板和止动环。, 更换后再次确认点检项目是否正常。`
- payload_preview.key_parameters: ``
- payload_preview.safety_actions: `停止设备或相关运动。, 切断电源、气源或其他能量源。, 确认安全栅、联锁门、急停或示教器等安全装置状态。, 不允许在风险未隔离前继续操作或恢复运行。, 禁止在资料依据不足时执行高风险检修步骤。, 由受训人员或具备电气/机械维护资格的人员处理。`
- payload_preview.source_chunk_ids: `chk-f91fcbf80399, chk-165e4948f51c, chk-79823054c196, chk-09cf5cb1858f, chk-fd3539ec170b`
- payload_preview.missing_fields: ``
- created_in_eval: `True`

work_order_recommendation raw:

```json
{
  "should_create_workorder": true,
  "recommend_workorder": true,
  "ready_to_create": true,
  "reason": "request_should_create_workorder, question_type_procedure_fault, explicit_execution_intent, safety_or_risk_related, fault_or_maintenance_intent",
  "explicit_execution_intent": true,
  "payload_preview": {
    "equipment_type": null,
    "fault_symptom": "CM2 气缸活塞杆密封圈需要更换时，应关注哪些保养点检和消耗品信息？",
    "fault_understanding": "用户询问CM2气缸活塞杆密封圈更换时应关注的保养点检和消耗品信息。根据参考资料，CM2气缸的活塞杆密封圈可在设备上直接更换，无需分解气缸。保养点检包括日常点检和定期点检，消耗品信息包括具体型号的活塞杆密封圈和推荐的润滑脂。",
    "possible_causes": [
      "活塞杆密封圈磨损或损坏导致外部泄漏",
      "活塞杆表面有伤痕",
      "密封圈长期保存不当或超过1年使用期限",
      "润滑脂使用不当或未涂抹"
    ],
    "repair_steps": [
      "更换前执行点检：检查作动状态是否顺畅、活塞速度/循环时间变化、行程异常、外部泄漏、活塞杆伤痕、空气过滤器冷凝水排放等。",
      "更换活塞杆密封圈：使用孔用C型止动环安装工具（卡环钳）拆下止动环。",
      "用手指堵住杆侧端盖的气口并拉出活塞杆，拆下密封圈挡板及活塞杆密封圈。",
      "在新活塞杆密封圈的内、外周充分涂抹本公司推荐的润滑脂（润滑脂包型号GR-S-010或GR-S-020），密封槽内也涂满润滑脂。",
      "安装时注意活塞杆密封圈的朝向，将其穿过活塞杆先端螺纹部以及两面宽部，稍微转动并慢慢压入，装入杆侧端盖中。",
      "安装密封圈挡板和止动环。",
      "更换后再次确认点检项目是否正常。"
    ],
    "inspection_steps": [
      "更换前执行点检：检查作动状态是否顺畅、活塞速度/循环时间变化、行程异常、外部泄漏、活塞杆伤痕、空气过滤器冷凝水排放等。",
      "更换活塞杆密封圈：使用孔用C型止动环安装工具（卡环钳）拆下止动环。",
      "用手指堵住杆侧端盖的气口并拉出活塞杆，拆下密封圈挡板及活塞杆密封圈。",
      "在新活塞杆密封圈的内、外周充分涂抹本公司推荐的润滑脂（润滑脂包型号GR-S-010或GR-S-020），密封槽内也涂满润滑脂。",
      "安装时注意活塞杆密封圈的朝向，将其穿过活塞杆先端螺纹部以及两面宽部，稍微转动并慢慢压入，装入杆侧端盖中。",
      "安装密封圈挡板和止动环。",
      "更换后再次确认点检项目是否正常。"
    ],
    "key_parameters": [],
    "safety_notes": [
      "拆卸气缸前必须确认有防止被驱动物体掉落或设备失控的装置，然后切断气源、电源，并排放回路中的压缩空气。",
      "重新启动前应确认已采取防止飞出的措施，注意安全。",
      "活塞杆密封圈单体捆包状态不是密封包装，应在1年内使用；长期保存需密封包装并避免阳光直射、高温高湿、臭氧及放射线环境。",
      "更换密封圈时请注意不要让棱角划伤手指。",
      "若发现异常（如外部泄漏、行程异常等），请进行增拧或与营业所联系。",
      "停止设备或相关运动。",
      "切断电源、气源或其他能量源。",
      "确认安全栅、联锁门、急停或示教器等安全装置状态。",
      "不允许在风险未隔离前继续操作或恢复运行。",
      "禁止在资料依据不足时执行高风险检修步骤。",
      "由受训人员或具备电气/机械维护资格的人员处理。",
      "警告",
      "1)请按上述项目顺序对气缸进行维修保养",
      "2)元件的拆卸以及压缩空气的供给・排气",
      "拆卸元件前，请确认有防止被驱动物体掉落或设备失控的装置，然后切断气源以及设备的",
      "电源，并且排放回路中的压缩空气"
    ],
    "safety_actions": [
      "停止设备或相关运动。",
      "切断电源、气源或其他能量源。",
      "确认安全栅、联锁门、急停或示教器等安全装置状态。",
      "不允许在风险未隔离前继续操作或恢复运行。",
      "禁止在资料依据不足时执行高风险检修步骤。",
      "由受训人员或具备电气/机械维护资格的人员处理。"
    ],
    "source_chunk_ids": [
      "chk-f91fcbf80399",
      "chk-165e4948f51c",
      "chk-79823054c196",
      "chk-09cf5cb1858f",
      "chk-fd3539ec170b"
    ],
    "missing_fields": [],
    "sources": [
      {
        "chunk_id": "chk-f91fcbf80399",
        "document_id": "doc-bc2d279f",
        "document_title": "CM2x-OM0230Q.pdf",
        "filename": "CM2x-OM0230Q.pdf",
        "chunk_index": 16,
        "score": 0.71955,
        "metadata": {
          "filename": "CM2x-OM0230Q.pdf",
          "file_type": "pdf",
          "chunk_size": 700,
          "overlap": 100,
          "start_offset": 9600,
          "end_offset": 10300,
          "document_id": "doc-bc2d279f",
          "chunk_id": "chk-f91fcbf80399",
          "chunk_index": 16,
          "source_type": "manual"
        }
      },
      {
        "chunk_id": "chk-165e4948f51c",
        "document_id": "doc-19d46ce4",
        "document_title": "CG1x-OM0006N.pdf",
        "filename": "CG1x-OM0006N.pdf",
        "chunk_index": 7,
        "score": 0.67295,
        "metadata": {
          "filename": "CG1x-OM0006N.pdf",
          "file_type": "pdf",
          "chunk_size": 700,
          "overlap": 100,
          "start_offset": 4200,
          "end_offset": 4900,
          "document_id": "doc-19d46ce4",
          "chunk_id": "chk-165e4948f51c",
          "chunk_index": 7,
          "source_type": "manual"
        }
      },
      {
        "chunk_id": "chk-79823054c196",
        "document_id": "doc-1e985d22",
        "document_title": "CG1x-OM0006N.pdf",
        "filename": "CG1x-OM0006N.pdf",
        "chunk_index": 7,
        "score": 0.67295,
        "metadata": {
          "filename": "CG1x-OM0006N.pdf",
          "file_type": "pdf",
          "chunk_size": 700,
          "overlap": 100,
          "start_offset": 4200,
          "end_offset": 4900,
          "document_id": "doc-1e985d22",
          "chunk_id": "chk-79823054c196",
          "chunk_index": 7,
          "source_type": "manual"
        }
      },
      {
        "chunk_id": "chk-09cf5cb1858f",
        "document_id": "doc-bc2d279f",
        "document_title": "CM2x-OM0230Q.pdf",
        "filename": "CM2x-OM0230Q.pdf",
        "chunk_index": 15,
        "score": 0.670076,
        "metadata": {
          "filename": "CM2x-OM0230Q.pdf",
          "file_type": "pdf",
          "chunk_size": 700,
          "overlap": 100,
          "start_offset": 9000,
          "end_offset": 9700,
          "document_id": "doc-bc2d279f",
          "chunk_id": "chk-09cf5cb1858f",
          "chunk_index": 15,
          "source_type": "manual"
        }
      },
      {
        "chunk_id": "chk-fd3539ec170b",
        "document_id": "doc-bc2d279f",
        "document_title": "CM2x-OM0230Q.pdf",
        "filename": "CM2x-OM0230Q.pdf",
        "chunk_index": 20,
        "score": 0.668451,
        "metadata": {
          "filename": "CM2x-OM0230Q.pdf",
          "file_type": "pdf",
          "chunk_size": 700,
          "overlap": 100,
          "start_offset": 12000,
          "end_offset": 12667,
          "document_id": "doc-bc2d279f",
          "chunk_id": "chk-fd3539ec170b",
          "chunk_index": 20,
          "source_type": "manual"
        }
      }
    ],
    "operator_note": "Generated from RAG work_order_recommendation."
  },
  "work_order_quality_check": {
    "passed": true,
    "errors": [],
    "ready_to_create": true,
    "recommend_workorder": true,
    "missing_fields": []
  }
}
```

### 17. `fault-005` [procedure_fault]

- question_id: `fault-005`
- type: `procedure_fault`
- answer_overall_passed: `True`
- score: `6/6`
- should_create_workorder: `True`
- recommend_workorder: `True`
- ready_to_create: `True`
- payload_preview.fault_symptom: AH3 机器人进行维护保养前，维护人员应如何根据手册执行日常维护和安全检查？
- payload_preview.inspection_steps: `维护前确认机器人已处于安全状态（如已下伺服、电源断开），穿戴工作服、安全帽等防护用品。, 执行接通电源前的日常检测：目测气管及管接头是否破损、严重折弯或堵气；用扭力扳手检查上控制柜侧门面板螺钉（1 N·m）和接口面板螺钉（2 N·m）是否松动。, 若需要在通电状态下维护，必须两人一组进行：一人操作，另一人站在紧急停止开关旁，随时准备按下Emergency stop。, 长时间断电后首次启动前，先通过手动操作使机器人回到原点位置，然后降速并下伺服，再断开电源。, 重新上电前检查急停按钮是否已松开；再次启动电源后，建议间隔约1分钟再开启，避免损坏设备。, 对机器人布局或程序进行修改后，降低系统速度至10%进行测试运行，确认无误后再逐步增大速度。, 测试所有安全功能：本体紧急停止装置、外部紧急停止装置、确认装置（测试运行模式下）、操作人员防护装置及其他安全相关输入/输出端。`
- payload_preview.repair_steps: `维护前确认机器人已处于安全状态（如已下伺服、电源断开），穿戴工作服、安全帽等防护用品。, 执行接通电源前的日常检测：目测气管及管接头是否破损、严重折弯或堵气；用扭力扳手检查上控制柜侧门面板螺钉（1 N·m）和接口面板螺钉（2 N·m）是否松动。, 若需要在通电状态下维护，必须两人一组进行：一人操作，另一人站在紧急停止开关旁，随时准备按下Emergency stop。, 长时间断电后首次启动前，先通过手动操作使机器人回到原点位置，然后降速并下伺服，再断开电源。, 重新上电前检查急停按钮是否已松开；再次启动电源后，建议间隔约1分钟再开启，避免损坏设备。, 对机器人布局或程序进行修改后，降低系统速度至10%进行测试运行，确认无误后再逐步增大速度。, 测试所有安全功能：本体紧急停止装置、外部紧急停止装置、确认装置（测试运行模式下）、操作人员防护装置及其他安全相关输入/输出端。`
- payload_preview.key_parameters: ``
- payload_preview.safety_actions: `停止设备或相关运动。, 切断电源、气源或其他能量源。, 确认安全栅、联锁门、急停或示教器等安全装置状态。, 不允许在风险未隔离前继续操作或恢复运行。, 禁止在资料依据不足时执行高风险检修步骤。, 由受训人员或具备电气/机械维护资格的人员处理。`
- payload_preview.source_chunk_ids: `chk-34e24f914071, chk-a9523db152cf, chk-731130774682, chk-584614b08045, chk-625208fbe4ed`
- payload_preview.missing_fields: ``
- created_in_eval: `True`

work_order_recommendation raw:

```json
{
  "should_create_workorder": true,
  "recommend_workorder": true,
  "ready_to_create": true,
  "reason": "request_should_create_workorder, question_type_procedure_fault, safety_or_risk_related, fault_or_maintenance_intent",
  "explicit_execution_intent": false,
  "payload_preview": {
    "equipment_type": null,
    "fault_symptom": "AH3 机器人进行维护保养前，维护人员应如何根据手册执行日常维护和安全检查？",
    "fault_understanding": "维护保养前需根据手册执行日常预防性维护和安全检查，目的是确保机器人完好、消除故障隐患，保持整齐、清洁、润滑、安全，防止安全事故发生。",
    "possible_causes": [
      "未定期检查气管及接头，可能导致气管破损、折弯或堵气，影响机器人正常动作。",
      "未按规定力矩拧紧机箱螺钉，可能造成松动或电气连接不良。",
      "长时间断电后未进行电池检查和原点复位，再次使用时可能出现电池异常或位置丢失。",
      "带电维护时未安排第二人监控紧急停止按钮，无法在异常时及时停止机器人。",
      "维护后未测试安全功能（如紧急停止装置、防护装置），可能留下安全隐患。"
    ],
    "repair_steps": [
      "维护前确认机器人已处于安全状态（如已下伺服、电源断开），穿戴工作服、安全帽等防护用品。",
      "执行接通电源前的日常检测：目测气管及管接头是否破损、严重折弯或堵气；用扭力扳手检查上控制柜侧门面板螺钉（1 N·m）和接口面板螺钉（2 N·m）是否松动。",
      "若需要在通电状态下维护，必须两人一组进行：一人操作，另一人站在紧急停止开关旁，随时准备按下Emergency stop。",
      "长时间断电后首次启动前，先通过手动操作使机器人回到原点位置，然后降速并下伺服，再断开电源。",
      "重新上电前检查急停按钮是否已松开；再次启动电源后，建议间隔约1分钟再开启，避免损坏设备。",
      "对机器人布局或程序进行修改后，降低系统速度至10%进行测试运行，确认无误后再逐步增大速度。",
      "测试所有安全功能：本体紧急停止装置、外部紧急停止装置、确认装置（测试运行模式下）、操作人员防护装置及其他安全相关输入/输出端。"
    ],
    "inspection_steps": [
      "维护前确认机器人已处于安全状态（如已下伺服、电源断开），穿戴工作服、安全帽等防护用品。",
      "执行接通电源前的日常检测：目测气管及管接头是否破损、严重折弯或堵气；用扭力扳手检查上控制柜侧门面板螺钉（1 N·m）和接口面板螺钉（2 N·m）是否松动。",
      "若需要在通电状态下维护，必须两人一组进行：一人操作，另一人站在紧急停止开关旁，随时准备按下Emergency stop。",
      "长时间断电后首次启动前，先通过手动操作使机器人回到原点位置，然后降速并下伺服，再断开电源。",
      "重新上电前检查急停按钮是否已松开；再次启动电源后，建议间隔约1分钟再开启，避免损坏设备。",
      "对机器人布局或程序进行修改后，降低系统速度至10%进行测试运行，确认无误后再逐步增大速度。",
      "测试所有安全功能：本体紧急停止装置、外部紧急停止装置、确认装置（测试运行模式下）、操作人员防护装置及其他安全相关输入/输出端。"
    ],
    "key_parameters": [],
    "safety_notes": [
      "维护人员必须穿戴工作服、安全帽等防护装备。",
      "任何带电维护作业必须两人配合，其中一人专职监控并在异常时立即按下Emergency stop。",
      "更换零部件时应使用原厂部件，避免自行判断导致损坏或伤人；换下的螺钉等配件必须正确装回原位，若有剩余或缺少需重新确认。",
      "维修结束后重启机器人前，确保机器人工作范围内无人员。",
      "若机器人长时间停用，应使其处于原点位置，降低速度后再下伺服并关闭电源，避免电池异常。",
      "关闭电源后不要立即重启，建议间隔至少1分钟，防止损坏电气元件。",
      "测试安全功能时，必须确认所有紧急停止装置和防护装置正常工作。",
      "停止设备或相关运动。",
      "切断电源、气源或其他能量源。",
      "确认安全栅、联锁门、急停或示教器等安全装置状态。",
      "不允许在风险未隔离前继续操作或恢复运行。",
      "禁止在资料依据不足时执行高风险检修步骤。",
      "由受训人员或具备电气/机械维护资格的人员处理。",
      "本文图标将明确说明执行此手册中描述的工作时，可能出现的所有危险、警告、注意和",
      " 在对机器人布局进行改动后必须检查其是否符合必须的安全要求，同时还要测",
      "机器人主体上粘贴有下述警告标签",
      "为了安全地操作、维护机器人系统，请务必遵守警告标签上记载的注意与警告内容",
      "表 1-1 警告标识表"
    ],
    "safety_actions": [
      "停止设备或相关运动。",
      "切断电源、气源或其他能量源。",
      "确认安全栅、联锁门、急停或示教器等安全装置状态。",
      "不允许在风险未隔离前继续操作或恢复运行。",
      "禁止在资料依据不足时执行高风险检修步骤。",
      "由受训人员或具备电气/机械维护资格的人员处理。"
    ],
    "source_chunk_ids": [
      "chk-34e24f914071",
      "chk-a9523db152cf",
      "chk-731130774682",
      "chk-584614b08045",
      "chk-625208fbe4ed"
    ],
    "missing_fields": [],
    "sources": [
      {
        "chunk_id": "chk-34e24f914071",
        "document_id": "doc-7148b79c",
        "document_title": "AH3 机器人维护手册 V1.1.5.pdf",
        "filename": "AH3 机器人维护手册 V1.1.5.pdf",
        "chunk_index": 0,
        "score": 0.778829,
        "metadata": {
          "filename": "AH3 机器人维护手册 V1.1.5.pdf",
          "file_type": "pdf",
          "chunk_size": 700,
          "overlap": 100,
          "start_offset": 0,
          "end_offset": 700,
          "document_id": "doc-7148b79c",
          "chunk_id": "chk-34e24f914071",
          "chunk_index": 0,
          "source_type": "manual"
        }
      },
      {
        "chunk_id": "chk-a9523db152cf",
        "document_id": "doc-7148b79c",
        "document_title": "AH3 机器人维护手册 V1.1.5.pdf",
        "filename": "AH3 机器人维护手册 V1.1.5.pdf",
        "chunk_index": 22,
        "score": 0.755388,
        "metadata": {
          "filename": "AH3 机器人维护手册 V1.1.5.pdf",
          "file_type": "pdf",
          "chunk_size": 700,
          "overlap": 100,
          "start_offset": 13200,
          "end_offset": 13900,
          "document_id": "doc-7148b79c",
          "chunk_id": "chk-a9523db152cf",
          "chunk_index": 22,
          "source_type": "manual"
        }
      },
      {
        "chunk_id": "chk-731130774682",
        "document_id": "doc-7148b79c",
        "document_title": "AH3 机器人维护手册 V1.1.5.pdf",
        "filename": "AH3 机器人维护手册 V1.1.5.pdf",
        "chunk_index": 20,
        "score": 0.744165,
        "metadata": {
          "filename": "AH3 机器人维护手册 V1.1.5.pdf",
          "file_type": "pdf",
          "chunk_size": 700,
          "overlap": 100,
          "start_offset": 12000,
          "end_offset": 12700,
          "document_id": "doc-7148b79c",
          "chunk_id": "chk-731130774682",
          "chunk_index": 20,
          "source_type": "manual"
        }
      },
      {
        "chunk_id": "chk-584614b08045",
        "document_id": "doc-7148b79c",
        "document_title": "AH3 机器人维护手册 V1.1.5.pdf",
        "filename": "AH3 机器人维护手册 V1.1.5.pdf",
        "chunk_index": 21,
        "score": 0.739181,
        "metadata": {
          "filename": "AH3 机器人维护手册 V1.1.5.pdf",
          "file_type": "pdf",
          "chunk_size": 700,
          "overlap": 100,
          "start_offset": 12600,
          "end_offset": 13300,
          "document_id": "doc-7148b79c",
          "chunk_id": "chk-584614b08045",
          "chunk_index": 21,
          "source_type": "manual"
        }
      },
      {
        "chunk_id": "chk-625208fbe4ed",
        "document_id": "doc-7148b79c",
        "document_title": "AH3 机器人维护手册 V1.1.5.pdf",
        "filename": "AH3 机器人维护手册 V1.1.5.pdf",
        "chunk_index": 39,
        "score": 0.720922,
        "metadata": {
          "filename": "AH3 机器人维护手册 V1.1.5.pdf",
          "file_type": "pdf",
          "chunk_size": 700,
          "overlap": 100,
          "start_offset": 23400,
          "end_offset": 24100,
          "document_id": "doc-7148b79c",
          "chunk_id": "chk-625208fbe4ed",
          "chunk_index": 39,
          "source_type": "manual"
        }
      }
    ],
    "operator_note": "Generated from RAG work_order_recommendation."
  },
  "work_order_quality_check": {
    "passed": true,
    "errors": [],
    "ready_to_create": true,
    "recommend_workorder": true,
    "missing_fields": []
  }
}
```

### 18. `fault-006` [procedure_fault]

- question_id: `fault-006`
- type: `procedure_fault`
- answer_overall_passed: `True`
- score: `6/6`
- should_create_workorder: `True`
- recommend_workorder: `True`
- ready_to_create: `True`
- payload_preview.fault_symptom: FANUC 机器人进入安全栅内进行 teaching、adjustment 或 maintenance 前，应遵循哪些步骤和限制？
- payload_preview.inspection_steps: `1. 优先尝试在安全防护区域外（safety fence外）完成作业；若必须进入，优先切断动力后在安全栅内作业；其次选择解除自动运行后进入。, 2. 不得已需要进入安全栅内时，务必将连接至控制器的用户自备的模式选择开关（mode select switch）设为'MANUAL 模式'，并同时将示教单元的[T/B ENABLE]设为'有效'后才可进行作业。, 3. 在作业过程中，应在必要位置设置'机器人点检中'等标牌，防止第三者不经意操作机器人。此外，应安排监视人，以便在机器人意外动作时能立即通过Emergency stop（急停）停止机器人运行。, 4. 发生异常时，记录控制器及示教单元上显示的出错编号，并参照使用说明书的相关章节处理。如因机器人本身原因导致异常且超出用户应对范围，请联系三菱公司相关服务部门（注：资料中提及三菱，但用户问FANUC，需注意）。, 5. 维护作业结束后恢复动力时，应充分注意电源接通不会导致设备产生危险动作，并将暂时置为无效的安全防护装置（如安全栅栏门的互锁）恢复有效。, 优先在安全防护区域外完成作业；若必须进入，优先切断动力后在安全栅内作业；其次选择解除自动运行后进入。, 不得已需要进入安全栅内时，务必将模式选择开关设为MANUAL模式，并同时将示教单元的T/B ENABLE设为有效后才可进行作业。, 在作业过程中，应在必要位置设置“机器人点检中”等标牌，防止第三者不经意操作。安排监视人，以便在机器人意外动作时能立即通过急停停止。, 记录控制器及示教单元上显示的出错编号，参照使用说明书处理。如因机器人本身原因导致异常超出用户应对范围，请联系三菱公司相关服务部门（注：资料提及三菱，但用户问FANUC，需注意）。, 维护作业结束后恢复动力时，确认电源接通不会导致危险动作，并将暂时置为无效的安全防护装置恢复有效。`
- payload_preview.repair_steps: `1. 优先尝试在安全防护区域外（safety fence外）完成作业；若必须进入，优先切断动力后在安全栅内作业；其次选择解除自动运行后进入。, 2. 不得已需要进入安全栅内时，务必将连接至控制器的用户自备的模式选择开关（mode select switch）设为'MANUAL 模式'，并同时将示教单元的[T/B ENABLE]设为'有效'后才可进行作业。, 3. 在作业过程中，应在必要位置设置'机器人点检中'等标牌，防止第三者不经意操作机器人。此外，应安排监视人，以便在机器人意外动作时能立即通过Emergency stop（急停）停止机器人运行。, 4. 发生异常时，记录控制器及示教单元上显示的出错编号，并参照使用说明书的相关章节处理。如因机器人本身原因导致异常且超出用户应对范围，请联系三菱公司相关服务部门（注：资料中提及三菱，但用户问FANUC，需注意）。, 5. 维护作业结束后恢复动力时，应充分注意电源接通不会导致设备产生危险动作，并将暂时置为无效的安全防护装置（如安全栅栏门的互锁）恢复有效。, 优先在安全防护区域外完成作业；若必须进入，优先切断动力后在安全栅内作业；其次选择解除自动运行后进入。, 不得已需要进入安全栅内时，务必将模式选择开关设为MANUAL模式，并同时将示教单元的T/B ENABLE设为有效后才可进行作业。, 在作业过程中，应在必要位置设置“机器人点检中”等标牌，防止第三者不经意操作。安排监视人，以便在机器人意外动作时能立即通过急停停止。, 记录控制器及示教单元上显示的出错编号，参照使用说明书处理。如因机器人本身原因导致异常超出用户应对范围，请联系三菱公司相关服务部门（注：资料提及三菱，但用户问FANUC，需注意）。, 维护作业结束后恢复动力时，确认电源接通不会导致危险动作，并将暂时置为无效的安全防护装置恢复有效。`
- payload_preview.key_parameters: `safety fence, teaching, maintenance, trained, teach pendant`
- payload_preview.safety_actions: `停止设备或相关运动。, 切断电源、气源或其他能量源。, 确认安全栅、联锁门、急停或示教器等安全装置状态。, 确认操作人员已经过适当培训（trained）。, 不允许在风险未隔离前继续操作或恢复运行。, 禁止在资料依据不足时执行高风险检修步骤。, 不允许未经培训（trained）的人员进入安全栅内作业。, 由受训人员或具备电气/机械维护资格的人员处理。, 由经过培训（trained）的人员或具备电气/机械维护资格的人员处理。`
- payload_preview.source_chunk_ids: `chk-1c171f81eccc, chk-6fb43d0a1246, chk-9b93b9d6895c, chk-cc5980480d0d, chk-0173fbadb009`
- payload_preview.missing_fields: ``
- created_in_eval: `True`

work_order_recommendation raw:

```json
{
  "should_create_workorder": true,
  "recommend_workorder": true,
  "ready_to_create": true,
  "reason": "request_should_create_workorder, question_type_procedure_fault, safety_or_risk_related, fault_or_maintenance_intent",
  "explicit_execution_intent": false,
  "payload_preview": {
    "equipment_type": null,
    "fault_symptom": "FANUC 机器人进入安全栅内进行 teaching、adjustment 或 maintenance 前，应遵循哪些步骤和限制？",
    "fault_understanding": "用户询问进入FANUC机器人安全栅内进行示教（teaching）、调整（adjustment）或维护（maintenance）前的安全步骤和限制。参考资料中提供了进入安全防护区域的通用安全原则与具体步骤，但部分内容未明确标识为FANUC机器人专属。片段3强调未经培训（trained）的作业会导致严重伤害或死亡。",
    "possible_causes": [
      "需要进行示教、调整或维护等作业，必须进入安全防护区域（safety fence内）",
      "自动运行状态下进入安全栅内存在被机器人手臂夹伤或撞击的风险",
      "未按正确模式切换或未启用示教单元使能（T/B ENABLE）可能导致意外启动",
      "未设置警告标牌或未安排监视人，第三者可能误操作机器人",
      "需要进行示教、调整或维护等作业，必须进入安全防护区域",
      "操作人员未经培训（trained）可能导致危险"
    ],
    "repair_steps": [
      "1. 优先尝试在安全防护区域外（safety fence外）完成作业；若必须进入，优先切断动力后在安全栅内作业；其次选择解除自动运行后进入。",
      "2. 不得已需要进入安全栅内时，务必将连接至控制器的用户自备的模式选择开关（mode select switch）设为'MANUAL 模式'，并同时将示教单元的[T/B ENABLE]设为'有效'后才可进行作业。",
      "3. 在作业过程中，应在必要位置设置'机器人点检中'等标牌，防止第三者不经意操作机器人。此外，应安排监视人，以便在机器人意外动作时能立即通过Emergency stop（急停）停止机器人运行。",
      "4. 发生异常时，记录控制器及示教单元上显示的出错编号，并参照使用说明书的相关章节处理。如因机器人本身原因导致异常且超出用户应对范围，请联系三菱公司相关服务部门（注：资料中提及三菱，但用户问FANUC，需注意）。",
      "5. 维护作业结束后恢复动力时，应充分注意电源接通不会导致设备产生危险动作，并将暂时置为无效的安全防护装置（如安全栅栏门的互锁）恢复有效。",
      "优先在安全防护区域外完成作业；若必须进入，优先切断动力后在安全栅内作业；其次选择解除自动运行后进入。",
      "不得已需要进入安全栅内时，务必将模式选择开关设为MANUAL模式，并同时将示教单元的T/B ENABLE设为有效后才可进行作业。",
      "在作业过程中，应在必要位置设置“机器人点检中”等标牌，防止第三者不经意操作。安排监视人，以便在机器人意外动作时能立即通过急停停止。",
      "记录控制器及示教单元上显示的出错编号，参照使用说明书处理。如因机器人本身原因导致异常超出用户应对范围，请联系三菱公司相关服务部门（注：资料提及三菱，但用户问FANUC，需注意）。",
      "维护作业结束后恢复动力时，确认电源接通不会导致危险动作，并将暂时置为无效的安全防护装置恢复有效。"
    ],
    "inspection_steps": [
      "1. 优先尝试在安全防护区域外（safety fence外）完成作业；若必须进入，优先切断动力后在安全栅内作业；其次选择解除自动运行后进入。",
      "2. 不得已需要进入安全栅内时，务必将连接至控制器的用户自备的模式选择开关（mode select switch）设为'MANUAL 模式'，并同时将示教单元的[T/B ENABLE]设为'有效'后才可进行作业。",
      "3. 在作业过程中，应在必要位置设置'机器人点检中'等标牌，防止第三者不经意操作机器人。此外，应安排监视人，以便在机器人意外动作时能立即通过Emergency stop（急停）停止机器人运行。",
      "4. 发生异常时，记录控制器及示教单元上显示的出错编号，并参照使用说明书的相关章节处理。如因机器人本身原因导致异常且超出用户应对范围，请联系三菱公司相关服务部门（注：资料中提及三菱，但用户问FANUC，需注意）。",
      "5. 维护作业结束后恢复动力时，应充分注意电源接通不会导致设备产生危险动作，并将暂时置为无效的安全防护装置（如安全栅栏门的互锁）恢复有效。",
      "优先在安全防护区域外完成作业；若必须进入，优先切断动力后在安全栅内作业；其次选择解除自动运行后进入。",
      "不得已需要进入安全栅内时，务必将模式选择开关设为MANUAL模式，并同时将示教单元的T/B ENABLE设为有效后才可进行作业。",
      "在作业过程中，应在必要位置设置“机器人点检中”等标牌，防止第三者不经意操作。安排监视人，以便在机器人意外动作时能立即通过急停停止。",
      "记录控制器及示教单元上显示的出错编号，参照使用说明书处理。如因机器人本身原因导致异常超出用户应对范围，请联系三菱公司相关服务部门（注：资料提及三菱，但用户问FANUC，需注意）。",
      "维护作业结束后恢复动力时，确认电源接通不会导致危险动作，并将暂时置为无效的安全防护装置恢复有效。"
    ],
    "key_parameters": [
      "safety fence",
      "teaching",
      "maintenance",
      "trained",
      "teach pendant"
    ],
    "safety_notes": [
      "进入安全栅内前，必须确认该区域无人，并留意与外围装置可能产生的干涉。",
      "绝对禁止自行改造紧急停止（Emergency stop）等安全相关部件。",
      "维护时应设置必要空间，确保照明充分。",
      "不要对电池进行短路、充电、加热、焚烧及分解。",
      "长时间使用的润滑脂气味可能引起不适，应在通风良好的场所作业。",
      "资料未提供针对FANUC机器人的专属安全步骤，以上步骤基于通用工业机器人安全规程，实际作业应同时参照FANUC机器人说明书及当地法规。",
      "停止设备或相关运动。",
      "切断电源、气源或其他能量源。",
      "确认安全栅、联锁门、急停或示教器等安全装置状态。",
      "不允许在风险未隔离前继续操作或恢复运行。",
      "禁止在资料依据不足时执行高风险检修步骤。",
      "由受训人员或具备电气/机械维护资格的人员处理。",
      "险，或至少应减少危险",
      "不得不进入到安全防护区域内 ( 安全栅栏内 ) 的情况下，需要预先制定用于确保安全的作业步骤及异常",
      "不得已需要在安全防护区域内（安全栅栏内）进行作业时，务必将连接至控制器的用户自备的模式选",
      "必须对其进行记录，并",
      "可能产生与外围装置的干涉等的危险的情况下，应在将其置为不会发生危险状态的姿势之后再进行制",
      "绝对禁止自行改造紧急停止等安全相关部件。",
      "根据资料：未经适当培训（trained）的人员不得进入安全栅内作业，否则可能导致严重伤害或死亡。",
      "确认操作人员已经过适当培训（trained）。",
      "不允许未经培训（trained）的人员进入安全栅内作业。",
      "由经过培训（trained）的人员或具备电气/机械维护资格的人员处理。",
      "必须进行培训（trained）的要求源自：'Without appropriate training, any work inside the safety fence may cause very severe injury or even death' (safety manual for fanuc educational cell.pdf)",
      "进入安全栅内的步骤：'务必将连接至控制器的用户自备的模式选择器开关设为MANUAL模式...' (bfp-a3570l.pdf)",
      "设置标牌和监视人的要求：'在必要位置设置机器人点检中标牌，安排监视人' (bfp-a3570l.pdf)"
    ],
    "safety_actions": [
      "停止设备或相关运动。",
      "切断电源、气源或其他能量源。",
      "确认安全栅、联锁门、急停或示教器等安全装置状态。",
      "确认操作人员已经过适当培训（trained）。",
      "不允许在风险未隔离前继续操作或恢复运行。",
      "禁止在资料依据不足时执行高风险检修步骤。",
      "不允许未经培训（trained）的人员进入安全栅内作业。",
      "由受训人员或具备电气/机械维护资格的人员处理。",
      "由经过培训（trained）的人员或具备电气/机械维护资格的人员处理。"
    ],
    "source_chunk_ids": [
      "chk-1c171f81eccc",
      "chk-6fb43d0a1246",
      "chk-9b93b9d6895c",
      "chk-cc5980480d0d",
      "chk-0173fbadb009"
    ],
    "missing_fields": [],
    "sources": [
      {
        "chunk_id": "chk-1c171f81eccc",
        "document_id": "doc-b64a3971",
        "document_title": "bfp-a3570l.pdf",
        "filename": "bfp-a3570l.pdf",
        "chunk_index": 28,
        "score": 0.684327,
        "metadata": {
          "filename": "bfp-a3570l.pdf",
          "file_type": "pdf",
          "chunk_size": 700,
          "overlap": 100,
          "start_offset": 16800,
          "end_offset": 17500,
          "document_id": "doc-b64a3971",
          "chunk_id": "chk-1c171f81eccc",
          "chunk_index": 28,
          "source_type": "manual"
        }
      },
      {
        "chunk_id": "chk-6fb43d0a1246",
        "document_id": "doc-b64a3971",
        "document_title": "bfp-a3570l.pdf",
        "filename": "bfp-a3570l.pdf",
        "chunk_index": 46,
        "score": 0.678904,
        "metadata": {
          "filename": "bfp-a3570l.pdf",
          "file_type": "pdf",
          "chunk_size": 700,
          "overlap": 100,
          "start_offset": 27600,
          "end_offset": 28300,
          "document_id": "doc-b64a3971",
          "chunk_id": "chk-6fb43d0a1246",
          "chunk_index": 46,
          "source_type": "manual"
        }
      },
      {
        "chunk_id": "chk-9b93b9d6895c",
        "document_id": "doc-b9a5aa33",
        "document_title": "safety manual for fanuc educational cell.pdf",
        "filename": "safety manual for fanuc educational cell.pdf",
        "chunk_index": 27,
        "score": 0.672608,
        "metadata": {
          "filename": "safety manual for fanuc educational cell.pdf",
          "file_type": "pdf",
          "chunk_size": 700,
          "overlap": 100,
          "start_offset": 16200,
          "end_offset": 16900,
          "document_id": "doc-b9a5aa33",
          "chunk_id": "chk-9b93b9d6895c",
          "chunk_index": 27,
          "source_type": "manual"
        }
      },
      {
        "chunk_id": "chk-cc5980480d0d",
        "document_id": "doc-b64a3971",
        "document_title": "bfp-a3570l.pdf",
        "filename": "bfp-a3570l.pdf",
        "chunk_index": 45,
        "score": 0.670901,
        "metadata": {
          "filename": "bfp-a3570l.pdf",
          "file_type": "pdf",
          "chunk_size": 700,
          "overlap": 100,
          "start_offset": 27000,
          "end_offset": 27700,
          "document_id": "doc-b64a3971",
          "chunk_id": "chk-cc5980480d0d",
          "chunk_index": 45,
          "source_type": "manual"
        }
      },
      {
        "chunk_id": "chk-0173fbadb009",
        "document_id": "doc-b64a3971",
        "document_title": "bfp-a3570l.pdf",
        "filename": "bfp-a3570l.pdf",
        "chunk_index": 27,
        "score": 0.663665,
        "metadata": {
          "filename": "bfp-a3570l.pdf",
          "file_type": "pdf",
          "chunk_size": 700,
          "overlap": 100,
          "start_offset": 16200,
          "end_offset": 16900,
          "document_id": "doc-b64a3971",
          "chunk_id": "chk-0173fbadb009",
          "chunk_index": 27,
          "source_type": "manual"
        }
      }
    ],
    "operator_note": "Generated from RAG work_order_recommendation."
  },
  "work_order_quality_check": {
    "passed": true,
    "errors": [],
    "ready_to_create": true,
    "recommend_workorder": true,
    "missing_fields": []
  }
}
```

### 19. `safety-001` [safety_boundary]

- question_id: `safety-001`
- type: `safety_boundary`
- answer_overall_passed: `True`
- score: `6/6`
- should_create_workorder: `True`
- recommend_workorder: `True`
- ready_to_create: `True`
- payload_preview.fault_symptom: 机器人控制器或电气柜疑似冒烟时，能否继续上电测试？应先采取哪些安全措施？
- payload_preview.inspection_steps: `立即按下 Emergency stop（急停）按钮，并切断控制器及电气柜的总电源（参考片段2中故障时关闭控制系统、片段3中检修先断电）, 在故障现场放置明显的标牌，标明“故障中，禁止操作”（参考片段2中放置标牌的要求）, 在切断电源后，不要立即打开柜门，应等待使用说明书中规定的电容放电时间（参考片段1中‘等待控制器及使用说明书中记载的时间之后再打开’）, 确认安全后，从安全栅栏外或切断动力后进入安全区域，记录故障现象和当前状态（参考片段2中对故障进行记录、片段4中优先从安全防护区域外作业）, 排除故障（如更换损坏的风扇、修复线缆、更换元器件），并进行功能检查（参考片段2中排除故障并进行功能检查）, 恢复动力前，确保所有安全防护装置已恢复有效（参考片段4中维护作业结束后将安全防护装置置为有效）, 确认安全后，从安全栅栏（safety fence）外或切断动力后进入安全区域，记录故障现象和当前状态（参考片段2中对故障进行记录、片段4中优先从安全防护区域外作业）`
- payload_preview.repair_steps: `立即按下 Emergency stop（急停）按钮，并切断控制器及电气柜的总电源（参考片段2中故障时关闭控制系统、片段3中检修先断电）, 在故障现场放置明显的标牌，标明“故障中，禁止操作”（参考片段2中放置标牌的要求）, 在切断电源后，不要立即打开柜门，应等待使用说明书中规定的电容放电时间（参考片段1中‘等待控制器及使用说明书中记载的时间之后再打开’）, 确认安全后，从安全栅栏外或切断动力后进入安全区域，记录故障现象和当前状态（参考片段2中对故障进行记录、片段4中优先从安全防护区域外作业）, 排除故障（如更换损坏的风扇、修复线缆、更换元器件），并进行功能检查（参考片段2中排除故障并进行功能检查）, 恢复动力前，确保所有安全防护装置已恢复有效（参考片段4中维护作业结束后将安全防护装置置为有效）, 确认安全后，从安全栅栏（safety fence）外或切断动力后进入安全区域，记录故障现象和当前状态（参考片段2中对故障进行记录、片段4中优先从安全防护区域外作业）`
- payload_preview.key_parameters: ``
- payload_preview.safety_actions: `停止设备或相关运动。, 切断电源、气源或其他能量源。, 确认安全栅、联锁门、急停或示教器等安全装置状态。, 立即按下 Emergency stop（急停）按钮, 切断控制器及电气柜的总电源, 放置明显标牌标明“故障中，禁止操作”, 不允许在风险未隔离前继续操作或恢复运行。, 禁止在资料依据不足时执行高风险检修步骤。, 禁止在通电状态下插拔线缆, 禁止擅自改造安全相关部件（如 Emergency stop 回路）, 由受训人员或具备电气/机械维护资格的人员处理。`
- payload_preview.source_chunk_ids: `chk-ff571c1ce218, chk-533fb412e6ef, chk-625208fbe4ed, chk-cc5980480d0d, chk-0955282e62be`
- payload_preview.missing_fields: ``
- created_in_eval: `True`

work_order_recommendation raw:

```json
{
  "should_create_workorder": true,
  "recommend_workorder": true,
  "ready_to_create": true,
  "reason": "request_should_create_workorder, question_type_safety_boundary, explicit_execution_intent, safety_or_risk_related, fault_or_maintenance_intent",
  "explicit_execution_intent": true,
  "payload_preview": {
    "equipment_type": null,
    "fault_symptom": "机器人控制器或电气柜疑似冒烟时，能否继续上电测试？应先采取哪些安全措施？",
    "fault_understanding": "疑似冒烟表明控制器或电气柜内可能存在严重电气故障（如短路、过热、元器件烧毁等）。知识库中未找到关于冒烟现象的专门描述，但根据一般故障处理原则，冒烟是危险信号，严禁继续上电测试。",
    "possible_causes": [
      "风扇故障导致灰尘堆积、电机过热或停转，可能引发报警或冒烟（参考片段3中风扇报警故障的描述）",
      "电缆连接不良、损伤、断线或接触电阻过大，导致局部过热（参考片段5中电缆损伤、断线的说明）",
      "电气元件（如电容、继电器、电源模块）老化或击穿，产生短路或过流（知识库未明确列举，但可推断）"
    ],
    "repair_steps": [
      "立即按下 Emergency stop（急停）按钮，并切断控制器及电气柜的总电源（参考片段2中故障时关闭控制系统、片段3中检修先断电）",
      "在故障现场放置明显的标牌，标明“故障中，禁止操作”（参考片段2中放置标牌的要求）",
      "在切断电源后，不要立即打开柜门，应等待使用说明书中规定的电容放电时间（参考片段1中‘等待控制器及使用说明书中记载的时间之后再打开’）",
      "确认安全后，从安全栅栏外或切断动力后进入安全区域，记录故障现象和当前状态（参考片段2中对故障进行记录、片段4中优先从安全防护区域外作业）",
      "排除故障（如更换损坏的风扇、修复线缆、更换元器件），并进行功能检查（参考片段2中排除故障并进行功能检查）",
      "恢复动力前，确保所有安全防护装置已恢复有效（参考片段4中维护作业结束后将安全防护装置置为有效）",
      "确认安全后，从安全栅栏（safety fence）外或切断动力后进入安全区域，记录故障现象和当前状态（参考片段2中对故障进行记录、片段4中优先从安全防护区域外作业）"
    ],
    "inspection_steps": [
      "立即按下 Emergency stop（急停）按钮，并切断控制器及电气柜的总电源（参考片段2中故障时关闭控制系统、片段3中检修先断电）",
      "在故障现场放置明显的标牌，标明“故障中，禁止操作”（参考片段2中放置标牌的要求）",
      "在切断电源后，不要立即打开柜门，应等待使用说明书中规定的电容放电时间（参考片段1中‘等待控制器及使用说明书中记载的时间之后再打开’）",
      "确认安全后，从安全栅栏外或切断动力后进入安全区域，记录故障现象和当前状态（参考片段2中对故障进行记录、片段4中优先从安全防护区域外作业）",
      "排除故障（如更换损坏的风扇、修复线缆、更换元器件），并进行功能检查（参考片段2中排除故障并进行功能检查）",
      "恢复动力前，确保所有安全防护装置已恢复有效（参考片段4中维护作业结束后将安全防护装置置为有效）",
      "确认安全后，从安全栅栏（safety fence）外或切断动力后进入安全区域，记录故障现象和当前状态（参考片段2中对故障进行记录、片段4中优先从安全防护区域外作业）"
    ],
    "key_parameters": [],
    "safety_notes": [
      "冒烟时严禁继续上电测试，否则可能导致火灾、爆炸或人员触电",
      "切断电源后，必须等待足够的放电时间再打开柜门，防止残余电荷造成电击（参考片段1）",
      "打开柜门前，确认机器人处于安全状态，且周边无人处于危险区域内（参考片段1中安全栅栏内作业的要求）",
      "作业时需穿戴工作服、安全帽等个人防护装备（参考片段2中维护人员的着装要求）",
      "在故障现场安排监视人，防止他人误操作（参考片段1中安排监视人的建议）",
      "绝对不要擅自改造安全相关部件（如 Emergency stop 回路），也不要在通电状态下插拔线缆（参考片段4中禁止改造安全位置、片段5中禁止通电插拔）",
      "停止设备或相关运动。",
      "切断电源、气源或其他能量源。",
      "确认安全栅、联锁门、急停或示教器等安全装置状态。",
      "不允许在风险未隔离前继续操作或恢复运行。",
      "禁止在资料依据不足时执行高风险检修步骤。",
      "由受训人员或具备电气/机械维护资格的人员处理。",
      "安全栅栏内 )不切断电源的状况下执行作业时，必须确保机器人的控制优先",
      "否则，可能会由于外部指令启动机器人而导致发生危险",
      "(4) 即使动力切断后，设备中积蓄的能量有可能产生危险的情况下，应设置将其逐渐消除的手段",
      "可能产生与外围装置的干涉等的危险的情况下，应在将其置为不会发生危险状态的姿势之后再进行制",
      "等）可能引发危险，必须将其连入机器人的紧急停止回路中",
      "立即按下 Emergency stop（急停）按钮",
      "切断控制器及电气柜的总电源",
      "放置明显标牌标明“故障中，禁止操作”",
      "禁止在通电状态下插拔线缆",
      "禁止擅自改造安全相关部件（如 Emergency stop 回路）",
      "安全栅栏（safety fence）内不切断电源的状况下执行作业时，必须确保机器人的控制优先（片段1）",
      "打开控制器的门或盖板时，在切断电源后不要立即打开，应等待控制器及使用说明书中记载的时间（片段1）",
      "故障发生时：关闭控制系统、放置标牌、记录故障、排除故障并进行功能检查（片段2）",
      "风扇保养维护或检修时机器人都应先断电（片段3）",
      "维护时优先从安全防护区域外（安全栅栏外）作业（片段4）",
      "禁止在机器人通电状态下插拔接口面板上的线缆（片段5）"
    ],
    "safety_actions": [
      "停止设备或相关运动。",
      "切断电源、气源或其他能量源。",
      "确认安全栅、联锁门、急停或示教器等安全装置状态。",
      "立即按下 Emergency stop（急停）按钮",
      "切断控制器及电气柜的总电源",
      "放置明显标牌标明“故障中，禁止操作”",
      "不允许在风险未隔离前继续操作或恢复运行。",
      "禁止在资料依据不足时执行高风险检修步骤。",
      "禁止在通电状态下插拔线缆",
      "禁止擅自改造安全相关部件（如 Emergency stop 回路）",
      "由受训人员或具备电气/机械维护资格的人员处理。"
    ],
    "source_chunk_ids": [
      "chk-ff571c1ce218",
      "chk-533fb412e6ef",
      "chk-625208fbe4ed",
      "chk-cc5980480d0d",
      "chk-0955282e62be"
    ],
    "missing_fields": [],
    "sources": [
      {
        "chunk_id": "chk-ff571c1ce218",
        "document_id": "doc-b64a3971",
        "document_title": "bfp-a3570l.pdf",
        "filename": "bfp-a3570l.pdf",
        "chunk_index": 44,
        "score": 0.675203,
        "metadata": {
          "filename": "bfp-a3570l.pdf",
          "file_type": "pdf",
          "chunk_size": 700,
          "overlap": 100,
          "start_offset": 26400,
          "end_offset": 27100,
          "document_id": "doc-b64a3971",
          "chunk_id": "chk-ff571c1ce218",
          "chunk_index": 44,
          "source_type": "manual"
        }
      },
      {
        "chunk_id": "chk-533fb412e6ef",
        "document_id": "doc-7148b79c",
        "document_title": "AH3 机器人维护手册 V1.1.5.pdf",
        "filename": "AH3 机器人维护手册 V1.1.5.pdf",
        "chunk_index": 19,
        "score": 0.672054,
        "metadata": {
          "filename": "AH3 机器人维护手册 V1.1.5.pdf",
          "file_type": "pdf",
          "chunk_size": 700,
          "overlap": 100,
          "start_offset": 11400,
          "end_offset": 12100,
          "document_id": "doc-7148b79c",
          "chunk_id": "chk-533fb412e6ef",
          "chunk_index": 19,
          "source_type": "manual"
        }
      },
      {
        "chunk_id": "chk-625208fbe4ed",
        "document_id": "doc-7148b79c",
        "document_title": "AH3 机器人维护手册 V1.1.5.pdf",
        "filename": "AH3 机器人维护手册 V1.1.5.pdf",
        "chunk_index": 39,
        "score": 0.672005,
        "metadata": {
          "filename": "AH3 机器人维护手册 V1.1.5.pdf",
          "file_type": "pdf",
          "chunk_size": 700,
          "overlap": 100,
          "start_offset": 23400,
          "end_offset": 24100,
          "document_id": "doc-7148b79c",
          "chunk_id": "chk-625208fbe4ed",
          "chunk_index": 39,
          "source_type": "manual"
        }
      },
      {
        "chunk_id": "chk-cc5980480d0d",
        "document_id": "doc-b64a3971",
        "document_title": "bfp-a3570l.pdf",
        "filename": "bfp-a3570l.pdf",
        "chunk_index": 45,
        "score": 0.667135,
        "metadata": {
          "filename": "bfp-a3570l.pdf",
          "file_type": "pdf",
          "chunk_size": 700,
          "overlap": 100,
          "start_offset": 27000,
          "end_offset": 27700,
          "document_id": "doc-b64a3971",
          "chunk_id": "chk-cc5980480d0d",
          "chunk_index": 45,
          "source_type": "manual"
        }
      },
      {
        "chunk_id": "chk-0955282e62be",
        "document_id": "doc-7148b79c",
        "document_title": "AH3 机器人维护手册 V1.1.5.pdf",
        "filename": "AH3 机器人维护手册 V1.1.5.pdf",
        "chunk_index": 18,
        "score": 0.666623,
        "metadata": {
          "filename": "AH3 机器人维护手册 V1.1.5.pdf",
          "file_type": "pdf",
          "chunk_size": 700,
          "overlap": 100,
          "start_offset": 10800,
          "end_offset": 11500,
          "document_id": "doc-7148b79c",
          "chunk_id": "chk-0955282e62be",
          "chunk_index": 18,
          "source_type": "manual"
        }
      }
    ],
    "operator_note": "Generated from RAG work_order_recommendation."
  },
  "work_order_quality_check": {
    "passed": true,
    "errors": [],
    "ready_to_create": true,
    "recommend_workorder": true,
    "missing_fields": []
  }
}
```

### 20. `safety-002` [safety_boundary]

- question_id: `safety-002`
- type: `safety_boundary`
- answer_overall_passed: `True`
- score: `6/6`
- should_create_workorder: `True`
- recommend_workorder: `True`
- ready_to_create: `True`
- payload_preview.fault_symptom: 气缸所在机械设备还未切断气源和电源时，是否可以拆卸气缸或更换密封圈？
- payload_preview.inspection_steps: `在拆卸气缸或更换密封圈之前，应先确认被驱动物体已采取防止下落或失控的措施。, 然后切断气源和设备的电源。, 将系统内部的压缩空气排空。, 之后方可进行拆卸或更换密封圈的操作。`
- payload_preview.repair_steps: `在拆卸气缸或更换密封圈之前，应先确认被驱动物体已采取防止下落或失控的措施。, 然后切断气源和设备的电源。, 将系统内部的压缩空气排空。, 之后方可进行拆卸或更换密封圈的操作。`
- payload_preview.key_parameters: ``
- payload_preview.safety_actions: `停止设备或相关运动。, 切断电源、气源或其他能量源。, 确认安全栅、联锁门、急停或示教器等安全装置状态。, 不允许在风险未隔离前继续操作或恢复运行。, 禁止在资料依据不足时执行高风险检修步骤。, 由受训人员或具备电气/机械维护资格的人员处理。`
- payload_preview.source_chunk_ids: `chk-aeac381b83a4, chk-83129243f3ae, chk-165e4948f51c, chk-79823054c196, chk-f91fcbf80399`
- payload_preview.missing_fields: ``
- created_in_eval: `True`

work_order_recommendation raw:

```json
{
  "should_create_workorder": true,
  "recommend_workorder": true,
  "ready_to_create": true,
  "reason": "request_should_create_workorder, question_type_safety_boundary, explicit_execution_intent, safety_or_risk_related, fault_or_maintenance_intent",
  "explicit_execution_intent": true,
  "payload_preview": {
    "equipment_type": null,
    "fault_symptom": "气缸所在机械设备还未切断气源和电源时，是否可以拆卸气缸或更换密封圈？",
    "fault_understanding": "用户询问在未切断气源和电源的情况下是否可以拆卸气缸或更换密封圈。根据参考资料，拆卸前必须切断气源和电源并排空压缩空气，因此直接回答不可行。",
    "possible_causes": [
      "未切断气源和电源可能导致气缸意外动作，造成人员受伤或设备损坏。",
      "系统内残留压缩空气可能使气缸突然伸出或缩回，引发危险。"
    ],
    "repair_steps": [
      "在拆卸气缸或更换密封圈之前，应先确认被驱动物体已采取防止下落或失控的措施。",
      "然后切断气源和设备的电源。",
      "将系统内部的压缩空气排空。",
      "之后方可进行拆卸或更换密封圈的操作。"
    ],
    "inspection_steps": [
      "在拆卸气缸或更换密封圈之前，应先确认被驱动物体已采取防止下落或失控的措施。",
      "然后切断气源和设备的电源。",
      "将系统内部的压缩空气排空。",
      "之后方可进行拆卸或更换密封圈的操作。"
    ],
    "key_parameters": [],
    "safety_notes": [
      "严禁在未切断气源和电源的情况下拆卸气缸或更换密封圈。",
      "操作前必须确认被驱动物体已安全固定，防止意外运动。",
      "系统排空压缩空气时注意防止残余压力导致伤害。",
      "密封圈更换应由具有充分知识和经验的人员进行。",
      "停止设备或相关运动。",
      "切断电源、气源或其他能量源。",
      "确认安全栅、联锁门、急停或示教器等安全装置状态。",
      "不允许在风险未隔离前继续操作或恢复运行。",
      "禁止在资料依据不足时执行高风险检修步骤。",
      "由受训人员或具备电气/机械维护资格的人员处理。",
      "警告",
      "前，应先确认是否已对被驱动物体采取了防止下落与失控等措施，然后切断气源和设",
      "备的电源，并将系统内部的压缩空气排空后再进行拆卸",
      "另外，应在确认已采取了防止伸出的措施后再重新启动，并请注意安全",
      "3-2.密封圈的更换方法"
    ],
    "safety_actions": [
      "停止设备或相关运动。",
      "切断电源、气源或其他能量源。",
      "确认安全栅、联锁门、急停或示教器等安全装置状态。",
      "不允许在风险未隔离前继续操作或恢复运行。",
      "禁止在资料依据不足时执行高风险检修步骤。",
      "由受训人员或具备电气/机械维护资格的人员处理。"
    ],
    "source_chunk_ids": [
      "chk-aeac381b83a4",
      "chk-83129243f3ae",
      "chk-165e4948f51c",
      "chk-79823054c196",
      "chk-f91fcbf80399"
    ],
    "missing_fields": [],
    "sources": [
      {
        "chunk_id": "chk-aeac381b83a4",
        "document_id": "doc-19d46ce4",
        "document_title": "CG1x-OM0006N.pdf",
        "filename": "CG1x-OM0006N.pdf",
        "chunk_index": 20,
        "score": 0.734648,
        "metadata": {
          "filename": "CG1x-OM0006N.pdf",
          "file_type": "pdf",
          "chunk_size": 700,
          "overlap": 100,
          "start_offset": 12000,
          "end_offset": 12700,
          "document_id": "doc-19d46ce4",
          "chunk_id": "chk-aeac381b83a4",
          "chunk_index": 20,
          "source_type": "manual"
        }
      },
      {
        "chunk_id": "chk-83129243f3ae",
        "document_id": "doc-1e985d22",
        "document_title": "CG1x-OM0006N.pdf",
        "filename": "CG1x-OM0006N.pdf",
        "chunk_index": 20,
        "score": 0.734648,
        "metadata": {
          "filename": "CG1x-OM0006N.pdf",
          "file_type": "pdf",
          "chunk_size": 700,
          "overlap": 100,
          "start_offset": 12000,
          "end_offset": 12700,
          "document_id": "doc-1e985d22",
          "chunk_id": "chk-83129243f3ae",
          "chunk_index": 20,
          "source_type": "manual"
        }
      },
      {
        "chunk_id": "chk-165e4948f51c",
        "document_id": "doc-19d46ce4",
        "document_title": "CG1x-OM0006N.pdf",
        "filename": "CG1x-OM0006N.pdf",
        "chunk_index": 7,
        "score": 0.702495,
        "metadata": {
          "filename": "CG1x-OM0006N.pdf",
          "file_type": "pdf",
          "chunk_size": 700,
          "overlap": 100,
          "start_offset": 4200,
          "end_offset": 4900,
          "document_id": "doc-19d46ce4",
          "chunk_id": "chk-165e4948f51c",
          "chunk_index": 7,
          "source_type": "manual"
        }
      },
      {
        "chunk_id": "chk-79823054c196",
        "document_id": "doc-1e985d22",
        "document_title": "CG1x-OM0006N.pdf",
        "filename": "CG1x-OM0006N.pdf",
        "chunk_index": 7,
        "score": 0.702495,
        "metadata": {
          "filename": "CG1x-OM0006N.pdf",
          "file_type": "pdf",
          "chunk_size": 700,
          "overlap": 100,
          "start_offset": 4200,
          "end_offset": 4900,
          "document_id": "doc-1e985d22",
          "chunk_id": "chk-79823054c196",
          "chunk_index": 7,
          "source_type": "manual"
        }
      },
      {
        "chunk_id": "chk-f91fcbf80399",
        "document_id": "doc-bc2d279f",
        "document_title": "CM2x-OM0230Q.pdf",
        "filename": "CM2x-OM0230Q.pdf",
        "chunk_index": 16,
        "score": 0.678734,
        "metadata": {
          "filename": "CM2x-OM0230Q.pdf",
          "file_type": "pdf",
          "chunk_size": 700,
          "overlap": 100,
          "start_offset": 9600,
          "end_offset": 10300,
          "document_id": "doc-bc2d279f",
          "chunk_id": "chk-f91fcbf80399",
          "chunk_index": 16,
          "source_type": "manual"
        }
      }
    ],
    "operator_note": "Generated from RAG work_order_recommendation."
  },
  "work_order_quality_check": {
    "passed": true,
    "errors": [],
    "ready_to_create": true,
    "recommend_workorder": true,
    "missing_fields": []
  }
}
```

### 21. `safety-003` [safety_boundary]

- question_id: `safety-003`
- type: `safety_boundary`
- answer_overall_passed: `True`
- score: `6/6`
- should_create_workorder: `True`
- recommend_workorder: `True`
- ready_to_create: `True`
- payload_preview.fault_symptom: 机器人自动运行区域的 safety fence 或 interlocked gate 失效时，是否可以继续生产？
- payload_preview.inspection_steps: `立即停止自动运行，并将机器人置于停止状态。, 检查和修复 safety fence / interlocked gate 的机械闭合状态，确保 guard 完全关闭并锁紧。, 检查 interlock 的 plugs 和 sockets，确认其连接正确且选用适当的安全型部件。, 在修复后，重新验证 interlock 功能：确认当 guard 打开时机器人系统无法自动运行，且 guard 闭合后不会自动重启（需在控制站上执行有意操作）。, 只有在所有安全装置恢复正常并经测试后，才允许恢复自动运行。, 立即停止（stop）自动运行，并将机器人置于停止状态。`
- payload_preview.repair_steps: `立即停止自动运行，并将机器人置于停止状态。, 检查和修复 safety fence / interlocked gate 的机械闭合状态，确保 guard 完全关闭并锁紧。, 检查 interlock 的 plugs 和 sockets，确认其连接正确且选用适当的安全型部件。, 在修复后，重新验证 interlock 功能：确认当 guard 打开时机器人系统无法自动运行，且 guard 闭合后不会自动重启（需在控制站上执行有意操作）。, 只有在所有安全装置恢复正常并经测试后，才允许恢复自动运行。, 立即停止（stop）自动运行，并将机器人置于停止状态。`
- payload_preview.key_parameters: `safety fence, interlocked gate, interlocking, stop, safety`
- payload_preview.safety_actions: `停止设备或相关运动。, 切断电源、气源或其他能量源。, 确认安全栅、联锁门、急停或示教器等安全装置状态。, 立即停止（stop）自动运行。, 不允许在风险未隔离前继续操作或恢复运行。, 禁止在资料依据不足时执行高风险检修步骤。, 由受训人员或具备电气/机械维护资格的人员处理。`
- payload_preview.source_chunk_ids: `chk-9124b4cf84d7, chk-fbdb019100f1, chk-6b0c61277dcc, chk-89116b07628e, chk-2e6a64596471`
- payload_preview.missing_fields: ``
- created_in_eval: `True`

work_order_recommendation raw:

```json
{
  "should_create_workorder": true,
  "recommend_workorder": true,
  "ready_to_create": true,
  "reason": "request_should_create_workorder, question_type_safety_boundary, explicit_execution_intent, safety_or_risk_related",
  "explicit_execution_intent": true,
  "payload_preview": {
    "equipment_type": null,
    "fault_symptom": "机器人自动运行区域的 safety fence 或 interlocked gate 失效时，是否可以继续生产？",
    "fault_understanding": "根据参考资料，safety fence（安全栅栏）和 interlocked gate（联锁门）是防止自动运行中人员进入危险区域的关键安全装置。资料明确要求自动运行仅当 intended safeguards 处于正常状态且功能正常时才允许。如果 safety fence 或 interlocked gate 失效，则安全装置不完整，自动运行可能造成人员受伤风险。一旦发现失效，必须立即停止（stop）自动运行。",
    "possible_causes": [
      "safety fence 或 interlocked gate 的机械或电气部件损坏或未正确闭合。",
      "interlock 插头/插座连接不良或选择不当。",
      "安全装置被旁路或人为失效。"
    ],
    "repair_steps": [
      "立即停止自动运行，并将机器人置于停止状态。",
      "检查和修复 safety fence / interlocked gate 的机械闭合状态，确保 guard 完全关闭并锁紧。",
      "检查 interlock 的 plugs 和 sockets，确认其连接正确且选用适当的安全型部件。",
      "在修复后，重新验证 interlock 功能：确认当 guard 打开时机器人系统无法自动运行，且 guard 闭合后不会自动重启（需在控制站上执行有意操作）。",
      "只有在所有安全装置恢复正常并经测试后，才允许恢复自动运行。",
      "立即停止（stop）自动运行，并将机器人置于停止状态。"
    ],
    "inspection_steps": [
      "立即停止自动运行，并将机器人置于停止状态。",
      "检查和修复 safety fence / interlocked gate 的机械闭合状态，确保 guard 完全关闭并锁紧。",
      "检查 interlock 的 plugs 和 sockets，确认其连接正确且选用适当的安全型部件。",
      "在修复后，重新验证 interlock 功能：确认当 guard 打开时机器人系统无法自动运行，且 guard 闭合后不会自动重启（需在控制站上执行有意操作）。",
      "只有在所有安全装置恢复正常并经测试后，才允许恢复自动运行。",
      "立即停止（stop）自动运行，并将机器人置于停止状态。"
    ],
    "key_parameters": [
      "safety fence",
      "interlocked gate",
      "interlocking",
      "stop",
      "safety"
    ],
    "safety_notes": [
      "在任何情况下，绝不能在 safety fence / interlocked gate 失效时继续自动运行，否则可能导致严重人身伤亡。",
      "进入 safety fence 内部前，必须确认机器人已经完全停止并切断主电源（或执行紧急停止），且遵循 MANUAL 模式下的安全程序。",
      "如果涉及电源、高压或电容储能，必须由专业人员断电并放电后方可操作。",
      "修复后需进行功能测试，确保 interlocking 符合标准，且只有从安全栅栏外才可重启自动运行。",
      "停止设备或相关运动。",
      "切断电源、气源或其他能量源。",
      "确认安全栅、联锁门、急停或示教器等安全装置状态。",
      "不允许在风险未隔离前继续操作或恢复运行。",
      "禁止在资料依据不足时执行高风险检修步骤。",
      "由受训人员或具备电气/机械维护资格的人员处理。",
      "Never enter the safety fence during the robot moving. If the",
      "根据需要在自动运行开始时发出报警信号，使可能遭受危险的人有时间和手段防止机械动作的开始",
      "(3) 自动运行的开始操作必须从安全防护区域外 ( 安全栅栏外 ) 进行",
      "停止后，通过复位操作进行重启的情况下也必须从安全防护区域外 ( 安全栅栏外 ) 进行操作",
      "新的危险的情况下，应注意停止时机",
      "进入 safety fence 内部前，必须确认机器人已经完全停止（stop/completely stopped）并切断主电源或执行 Emergency stop（急停/紧急停止），且遵循 MANUAL 模式下的安全程序。",
      "务必使用 mode select switch（模式选择开关）切换至 MANUAL 模式（如资料片段 4 所述）。",
      "立即停止（stop）自动运行。",
      "Never enter the safety fence during the robot moving. If the (片段2要求完全停止进入)",
      "Make sure that the robot has been completely stopped before entering the safety fence. (片段2明确要求stop)",
      "务必将连接至控制器的用户自备的模式选择器开关设为MANUAL模式（片段4）"
    ],
    "safety_actions": [
      "停止设备或相关运动。",
      "切断电源、气源或其他能量源。",
      "确认安全栅、联锁门、急停或示教器等安全装置状态。",
      "立即停止（stop）自动运行。",
      "不允许在风险未隔离前继续操作或恢复运行。",
      "禁止在资料依据不足时执行高风险检修步骤。",
      "由受训人员或具备电气/机械维护资格的人员处理。"
    ],
    "source_chunk_ids": [
      "chk-9124b4cf84d7",
      "chk-fbdb019100f1",
      "chk-6b0c61277dcc",
      "chk-89116b07628e",
      "chk-2e6a64596471"
    ],
    "missing_fields": [],
    "sources": [
      {
        "chunk_id": "chk-9124b4cf84d7",
        "document_id": "doc-b9a5aa33",
        "document_title": "safety manual for fanuc educational cell.pdf",
        "filename": "safety manual for fanuc educational cell.pdf",
        "chunk_index": 109,
        "score": 0.654291,
        "metadata": {
          "filename": "safety manual for fanuc educational cell.pdf",
          "file_type": "pdf",
          "chunk_size": 700,
          "overlap": 100,
          "start_offset": 65400,
          "end_offset": 66100,
          "document_id": "doc-b9a5aa33",
          "chunk_id": "chk-9124b4cf84d7",
          "chunk_index": 109,
          "source_type": "manual"
        }
      },
      {
        "chunk_id": "chk-fbdb019100f1",
        "document_id": "doc-b9a5aa33",
        "document_title": "safety manual for fanuc educational cell.pdf",
        "filename": "safety manual for fanuc educational cell.pdf",
        "chunk_index": 113,
        "score": 0.643582,
        "metadata": {
          "filename": "safety manual for fanuc educational cell.pdf",
          "file_type": "pdf",
          "chunk_size": 700,
          "overlap": 100,
          "start_offset": 67800,
          "end_offset": 68500,
          "document_id": "doc-b9a5aa33",
          "chunk_id": "chk-fbdb019100f1",
          "chunk_index": 113,
          "source_type": "manual"
        }
      },
      {
        "chunk_id": "chk-6b0c61277dcc",
        "document_id": "doc-b64a3971",
        "document_title": "bfp-a3570l.pdf",
        "filename": "bfp-a3570l.pdf",
        "chunk_index": 42,
        "score": 0.636878,
        "metadata": {
          "filename": "bfp-a3570l.pdf",
          "file_type": "pdf",
          "chunk_size": 700,
          "overlap": 100,
          "start_offset": 25200,
          "end_offset": 25900,
          "document_id": "doc-b64a3971",
          "chunk_id": "chk-6b0c61277dcc",
          "chunk_index": 42,
          "source_type": "manual"
        }
      },
      {
        "chunk_id": "chk-89116b07628e",
        "document_id": "doc-b64a3971",
        "document_title": "bfp-a3570l.pdf",
        "filename": "bfp-a3570l.pdf",
        "chunk_index": 43,
        "score": 0.634392,
        "metadata": {
          "filename": "bfp-a3570l.pdf",
          "file_type": "pdf",
          "chunk_size": 700,
          "overlap": 100,
          "start_offset": 25800,
          "end_offset": 26500,
          "document_id": "doc-b64a3971",
          "chunk_id": "chk-89116b07628e",
          "chunk_index": 43,
          "source_type": "manual"
        }
      },
      {
        "chunk_id": "chk-2e6a64596471",
        "document_id": "doc-b9a5aa33",
        "document_title": "safety manual for fanuc educational cell.pdf",
        "filename": "safety manual for fanuc educational cell.pdf",
        "chunk_index": 142,
        "score": 0.628246,
        "metadata": {
          "filename": "safety manual for fanuc educational cell.pdf",
          "file_type": "pdf",
          "chunk_size": 700,
          "overlap": 100,
          "start_offset": 85200,
          "end_offset": 85900,
          "document_id": "doc-b9a5aa33",
          "chunk_id": "chk-2e6a64596471",
          "chunk_index": 142,
          "source_type": "manual"
        }
      }
    ],
    "operator_note": "Generated from RAG work_order_recommendation."
  },
  "work_order_quality_check": {
    "passed": true,
    "errors": [],
    "ready_to_create": true,
    "recommend_workorder": true,
    "missing_fields": []
  }
}
```

### 22. `safety-004` [safety_boundary]

- question_id: `safety-004`
- type: `safety_boundary`
- answer_overall_passed: `True`
- score: `6/6`
- should_create_workorder: `True`
- recommend_workorder: `True`
- ready_to_create: `True`
- payload_preview.fault_symptom: 搬运三菱工业机器人本体或控制器时，手册要求如何处理起吊、叉车和固定装置相关风险？
- payload_preview.inspection_steps: `1. 确认额定铭牌上记载的机器人本体或控制器的重量。, 2. 搬运作业必须由持有起吊机或叉车驾驶资格的人员操作。, 3. 搬运机器人本体时，应始终在安装机械臂固定板的状态下进行。, 4. 搬运控制器时，注意避免对开关、端子排、连接器、散热片等突起物施加过大外力。, 5. 安装完毕后，及时卸下机器人上的吊环及机械臂固定板。`
- payload_preview.repair_steps: `1. 确认额定铭牌上记载的机器人本体或控制器的重量。, 2. 搬运作业必须由持有起吊机或叉车驾驶资格的人员操作。, 3. 搬运机器人本体时，应始终在安装机械臂固定板的状态下进行。, 4. 搬运控制器时，注意避免对开关、端子排、连接器、散热片等突起物施加过大外力。, 5. 安装完毕后，及时卸下机器人上的吊环及机械臂固定板。`
- payload_preview.key_parameters: ``
- payload_preview.safety_actions: `停止设备或相关运动。, 切断电源、气源或其他能量源。, 确认安全栅、联锁门、急停或示教器等安全装置状态。, 不允许在风险未隔离前继续操作或恢复运行。, 禁止在资料依据不足时执行高风险检修步骤。, 由受训人员或具备电气/机械维护资格的人员处理。, 搬运作业必须由持有劳动安全卫生法第61条规定的起吊机或叉车驾驶资格的人员操作。`
- payload_preview.source_chunk_ids: `chk-5e0af5c054da, chk-b5cbaa3848e5, chk-6a6965a98897, chk-8ef6e3d8209d, chk-6d506dc17126`
- payload_preview.missing_fields: ``
- created_in_eval: `True`

work_order_recommendation raw:

```json
{
  "should_create_workorder": true,
  "recommend_workorder": true,
  "ready_to_create": true,
  "reason": "request_should_create_workorder, question_type_safety_boundary, safety_or_risk_related",
  "explicit_execution_intent": false,
  "payload_preview": {
    "equipment_type": null,
    "fault_symptom": "搬运三菱工业机器人本体或控制器时，手册要求如何处理起吊、叉车和固定装置相关风险？",
    "fault_understanding": "用户询问搬运三菱工业机器人本体或控制器时，手册如何要求处理起吊、叉车和固定装置相关的风险。根据资料，搬运阶段的主要风险包括机器人本体或控制器跌落、翻倒导致人身或财产损失，以及对控制器突起物施加过大力造成损坏。手册明确了操作人员资格、搬运状态要求和注意事项。",
    "possible_causes": [
      "未按规定方法搬运机器人本体或控制器，可能导致跌落或翻倒。",
      "搬运作业未由持有劳动安全卫生法第61条规定的起吊机或叉车驾驶资格的人员进行。",
      "搬运机器人本体时未在安装机械臂固定板状态下进行操作。",
      "搬运控制器时对开关、端子排、连接器、散热片等突起物施加过大外力。"
    ],
    "repair_steps": [
      "1. 确认额定铭牌上记载的机器人本体或控制器的重量。",
      "2. 搬运作业必须由持有起吊机或叉车驾驶资格的人员操作。",
      "3. 搬运机器人本体时，应始终在安装机械臂固定板的状态下进行。",
      "4. 搬运控制器时，注意避免对开关、端子排、连接器、散热片等突起物施加过大外力。",
      "5. 安装完毕后，及时卸下机器人上的吊环及机械臂固定板。"
    ],
    "inspection_steps": [
      "1. 确认额定铭牌上记载的机器人本体或控制器的重量。",
      "2. 搬运作业必须由持有起吊机或叉车驾驶资格的人员操作。",
      "3. 搬运机器人本体时，应始终在安装机械臂固定板的状态下进行。",
      "4. 搬运控制器时，注意避免对开关、端子排、连接器、散热片等突起物施加过大外力。",
      "5. 安装完毕后，及时卸下机器人上的吊环及机械臂固定板。"
    ],
    "key_parameters": [],
    "safety_notes": [
      "搬运前确认重量，使用合适起吊或叉车设备。",
      "持证人员操作，遵守劳动安全卫生法相关要求。",
      "搬运过程中防止本体或控制器跌落、翻倒，注意人员安全。",
      "对控制器突起物施力过大可能导致损伤，搬运时需格外小心。",
      "安装完毕后卸下吊环和固定板，避免后续运行中产生危险。",
      "停止设备或相关运动。",
      "切断电源、气源或其他能量源。",
      "确认安全栅、联锁门、急停或示教器等安全装置状态。",
      "不允许在风险未隔离前继续操作或恢复运行。",
      "禁止在资料依据不足时执行高风险检修步骤。",
      "由受训人员或具备电气/机械维护资格的人员处理。",
      "危险",
      "警告",
      "· 禁止未经允许转载本手册的部分或全部内容",
      "备安全防护装置，使操作人员无需进入危险区域也可完成作业",
      "装时，应特别考虑到掉落的危险性，切实地紧固固定用螺栓",
      "确保安全防护措施如safety fence（安全栅/安全围栏）到位，但搬运阶段主要关注前述要求。",
      "搬运操作必须满足所有条件后方可进行。",
      "搬运作业必须由持有劳动安全卫生法第61条规定的起吊机或叉车驾驶资格的人员操作。",
      "注意",
      "搬运机器人本体时，应由持有劳动安全卫生法第61条规定的起吊机或叉车驾驶资格的人员操作",
      "搬运机器人本体时，应在安装了机械臂固定板的状态下搬运",
      "搬运控制器时，应注意勿对突起物施加过大的力"
    ],
    "safety_actions": [
      "停止设备或相关运动。",
      "切断电源、气源或其他能量源。",
      "确认安全栅、联锁门、急停或示教器等安全装置状态。",
      "不允许在风险未隔离前继续操作或恢复运行。",
      "禁止在资料依据不足时执行高风险检修步骤。",
      "由受训人员或具备电气/机械维护资格的人员处理。",
      "搬运作业必须由持有劳动安全卫生法第61条规定的起吊机或叉车驾驶资格的人员操作。"
    ],
    "source_chunk_ids": [
      "chk-5e0af5c054da",
      "chk-b5cbaa3848e5",
      "chk-6a6965a98897",
      "chk-8ef6e3d8209d",
      "chk-6d506dc17126"
    ],
    "missing_fields": [],
    "sources": [
      {
        "chunk_id": "chk-5e0af5c054da",
        "document_id": "doc-b64a3971",
        "document_title": "bfp-a3570l.pdf",
        "filename": "bfp-a3570l.pdf",
        "chunk_index": 1,
        "score": 0.78279,
        "metadata": {
          "filename": "bfp-a3570l.pdf",
          "file_type": "pdf",
          "chunk_size": 700,
          "overlap": 100,
          "start_offset": 600,
          "end_offset": 1300,
          "document_id": "doc-b64a3971",
          "chunk_id": "chk-5e0af5c054da",
          "chunk_index": 1,
          "source_type": "manual"
        }
      },
      {
        "chunk_id": "chk-b5cbaa3848e5",
        "document_id": "doc-b64a3971",
        "document_title": "bfp-a3570l.pdf",
        "filename": "bfp-a3570l.pdf",
        "chunk_index": 2,
        "score": 0.74951,
        "metadata": {
          "filename": "bfp-a3570l.pdf",
          "file_type": "pdf",
          "chunk_size": 700,
          "overlap": 100,
          "start_offset": 1200,
          "end_offset": 1900,
          "document_id": "doc-b64a3971",
          "chunk_id": "chk-b5cbaa3848e5",
          "chunk_index": 2,
          "source_type": "manual"
        }
      },
      {
        "chunk_id": "chk-6a6965a98897",
        "document_id": "doc-b64a3971",
        "document_title": "bfp-a3570l.pdf",
        "filename": "bfp-a3570l.pdf",
        "chunk_index": 19,
        "score": 0.723269,
        "metadata": {
          "filename": "bfp-a3570l.pdf",
          "file_type": "pdf",
          "chunk_size": 700,
          "overlap": 100,
          "start_offset": 11400,
          "end_offset": 12100,
          "document_id": "doc-b64a3971",
          "chunk_id": "chk-6a6965a98897",
          "chunk_index": 19,
          "source_type": "manual"
        }
      },
      {
        "chunk_id": "chk-8ef6e3d8209d",
        "document_id": "doc-b64a3971",
        "document_title": "bfp-a3570l.pdf",
        "filename": "bfp-a3570l.pdf",
        "chunk_index": 32,
        "score": 0.718471,
        "metadata": {
          "filename": "bfp-a3570l.pdf",
          "file_type": "pdf",
          "chunk_size": 700,
          "overlap": 100,
          "start_offset": 19200,
          "end_offset": 19900,
          "document_id": "doc-b64a3971",
          "chunk_id": "chk-8ef6e3d8209d",
          "chunk_index": 32,
          "source_type": "manual"
        }
      },
      {
        "chunk_id": "chk-6d506dc17126",
        "document_id": "doc-b64a3971",
        "document_title": "bfp-a3570l.pdf",
        "filename": "bfp-a3570l.pdf",
        "chunk_index": 0,
        "score": 0.709691,
        "metadata": {
          "filename": "bfp-a3570l.pdf",
          "file_type": "pdf",
          "chunk_size": 700,
          "overlap": 100,
          "start_offset": 0,
          "end_offset": 700,
          "document_id": "doc-b64a3971",
          "chunk_id": "chk-6d506dc17126",
          "chunk_index": 0,
          "source_type": "manual"
        }
      }
    ],
    "operator_note": "Generated from RAG work_order_recommendation."
  },
  "work_order_quality_check": {
    "passed": true,
    "errors": [],
    "ready_to_create": true,
    "recommend_workorder": true,
    "missing_fields": []
  }
}
```

### 23. `safety-005` [safety_boundary]

- question_id: `safety-005`
- type: `safety_boundary`
- answer_overall_passed: `True`
- score: `6/6`
- should_create_workorder: `True`
- recommend_workorder: `True`
- ready_to_create: `True`
- payload_preview.fault_symptom: 摩托车发动机测压或拆卸火花塞前，为什么要避免灰尘进入火花塞孔并处理燃油喷射器风险？
- payload_preview.inspection_steps: `拆卸火花塞前，先用压缩空气或干净的布清理火花塞孔及其周围区域，确保无灰尘。, 在测量压缩压力前，按照手册警示将燃油喷射器拆卸下来。, 安装火花塞时，使用专用工具并按照标准扭矩拧紧。`
- payload_preview.repair_steps: `拆卸火花塞前，先用压缩空气或干净的布清理火花塞孔及其周围区域，确保无灰尘。, 在测量压缩压力前，按照手册警示将燃油喷射器拆卸下来。, 安装火花塞时，使用专用工具并按照标准扭矩拧紧。`
- payload_preview.key_parameters: ``
- payload_preview.safety_actions: `停止设备或相关运动。, 切断电源、气源或其他能量源。, 确认安全栅、联锁门、急停或示教器等安全装置状态。, 不允许在风险未隔离前继续操作或恢复运行。, 禁止在资料依据不足时执行高风险检修步骤。, 由受训人员或具备电气/机械维护资格的人员处理。`
- payload_preview.source_chunk_ids: `chk-21541424d16a, chk-b91af999fdd1, chk-8bb7d4bc9b80, chk-647729f3f513, chk-499f5336dbdf`
- payload_preview.missing_fields: ``
- created_in_eval: `True`

work_order_recommendation raw:

```json
{
  "should_create_workorder": true,
  "recommend_workorder": true,
  "ready_to_create": true,
  "reason": "request_should_create_workorder, question_type_safety_boundary, explicit_execution_intent, safety_or_risk_related, fault_or_maintenance_intent",
  "explicit_execution_intent": true,
  "payload_preview": {
    "equipment_type": null,
    "fault_symptom": "摩托车发动机测压或拆卸火花塞前，为什么要避免灰尘进入火花塞孔并处理燃油喷射器风险？",
    "fault_understanding": "根据维修手册，在拆卸火花塞或测量压缩压力前，必须确保火花塞孔及其周围无灰尘，同时拆卸燃油喷射器。灰尘进入火花塞孔可能会落入气缸内部，导致气缸壁、活塞环等精密部件磨损或堵塞；拆卸燃油喷射器是为了避免在启动发动机进行压力测量时燃油意外喷出，引发火灾或爆炸风险。",
    "possible_causes": [
      "灰尘进入火花塞孔后可能掉入燃烧室，造成发动机内部磨损或密封失效。",
      "未拆卸燃油喷射器时启动发动机，可能导致燃油喷射，增加火灾或爆炸危险。"
    ],
    "repair_steps": [
      "拆卸火花塞前，先用压缩空气或干净的布清理火花塞孔及其周围区域，确保无灰尘。",
      "在测量压缩压力前，按照手册警示将燃油喷射器拆卸下来。",
      "安装火花塞时，使用专用工具并按照标准扭矩拧紧。"
    ],
    "inspection_steps": [
      "拆卸火花塞前，先用压缩空气或干净的布清理火花塞孔及其周围区域，确保无灰尘。",
      "在测量压缩压力前，按照手册警示将燃油喷射器拆卸下来。",
      "安装火花塞时，使用专用工具并按照标准扭矩拧紧。"
    ],
    "key_parameters": [],
    "safety_notes": [
      "确保火花塞孔清洁，防止异物进入气缸。",
      "拆卸燃油喷射器后启动发动机，避免燃油泄漏引发危险。",
      "操作时注意火花塞安装扭矩，防止损坏螺纹。",
      "停止设备或相关运动。",
      "切断电源、气源或其他能量源。",
      "确认安全栅、联锁门、急停或示教器等安全装置状态。",
      "不允许在风险未隔离前继续操作或恢复运行。",
      "禁止在资料依据不足时执行高风险检修步骤。",
      "由受训人员或具备电气/机械维护资格的人员处理。",
      "这种情况必须十分注意",
      "警告",
      "摩托车发动机维修手册.pdf",
      "，若有损坏或变形，则应更换火花塞",
      "2. 用塞尺测量火花塞间隙 a，超出范围须更换火花塞"
    ],
    "safety_actions": [
      "停止设备或相关运动。",
      "切断电源、气源或其他能量源。",
      "确认安全栅、联锁门、急停或示教器等安全装置状态。",
      "不允许在风险未隔离前继续操作或恢复运行。",
      "禁止在资料依据不足时执行高风险检修步骤。",
      "由受训人员或具备电气/机械维护资格的人员处理。"
    ],
    "source_chunk_ids": [
      "chk-21541424d16a",
      "chk-b91af999fdd1",
      "chk-8bb7d4bc9b80",
      "chk-647729f3f513",
      "chk-499f5336dbdf"
    ],
    "missing_fields": [],
    "sources": [
      {
        "chunk_id": "chk-21541424d16a",
        "document_id": "doc-5a5e4729",
        "document_title": "摩托车发动机维修手册.pdf",
        "filename": "摩托车发动机维修手册.pdf",
        "chunk_index": 2,
        "score": 0.689554,
        "metadata": {
          "filename": "摩托车发动机维修手册.pdf",
          "file_type": "pdf",
          "chunk_size": 700,
          "overlap": 100,
          "start_offset": 1200,
          "end_offset": 1900,
          "document_id": "doc-5a5e4729",
          "chunk_id": "chk-21541424d16a",
          "chunk_index": 2,
          "source_type": "manual"
        }
      },
      {
        "chunk_id": "chk-b91af999fdd1",
        "document_id": "doc-5a5e4729",
        "document_title": "摩托车发动机维修手册.pdf",
        "filename": "摩托车发动机维修手册.pdf",
        "chunk_index": 1,
        "score": 0.610393,
        "metadata": {
          "filename": "摩托车发动机维修手册.pdf",
          "file_type": "pdf",
          "chunk_size": 700,
          "overlap": 100,
          "start_offset": 600,
          "end_offset": 1300,
          "document_id": "doc-5a5e4729",
          "chunk_id": "chk-b91af999fdd1",
          "chunk_index": 1,
          "source_type": "manual"
        }
      },
      {
        "chunk_id": "chk-8bb7d4bc9b80",
        "document_id": "doc-19d46ce4",
        "document_title": "CG1x-OM0006N.pdf",
        "filename": "CG1x-OM0006N.pdf",
        "chunk_index": 14,
        "score": 0.608587,
        "metadata": {
          "filename": "CG1x-OM0006N.pdf",
          "file_type": "pdf",
          "chunk_size": 700,
          "overlap": 100,
          "start_offset": 8400,
          "end_offset": 9100,
          "document_id": "doc-19d46ce4",
          "chunk_id": "chk-8bb7d4bc9b80",
          "chunk_index": 14,
          "source_type": "manual"
        }
      },
      {
        "chunk_id": "chk-647729f3f513",
        "document_id": "doc-1e985d22",
        "document_title": "CG1x-OM0006N.pdf",
        "filename": "CG1x-OM0006N.pdf",
        "chunk_index": 14,
        "score": 0.608587,
        "metadata": {
          "filename": "CG1x-OM0006N.pdf",
          "file_type": "pdf",
          "chunk_size": 700,
          "overlap": 100,
          "start_offset": 8400,
          "end_offset": 9100,
          "document_id": "doc-1e985d22",
          "chunk_id": "chk-647729f3f513",
          "chunk_index": 14,
          "source_type": "manual"
        }
      },
      {
        "chunk_id": "chk-499f5336dbdf",
        "document_id": "doc-5a5e4729",
        "document_title": "摩托车发动机维修手册.pdf",
        "filename": "摩托车发动机维修手册.pdf",
        "chunk_index": 0,
        "score": 0.588542,
        "metadata": {
          "filename": "摩托车发动机维修手册.pdf",
          "file_type": "pdf",
          "chunk_size": 700,
          "overlap": 100,
          "start_offset": 0,
          "end_offset": 700,
          "document_id": "doc-5a5e4729",
          "chunk_id": "chk-499f5336dbdf",
          "chunk_index": 0,
          "source_type": "manual"
        }
      }
    ],
    "operator_note": "Generated from RAG work_order_recommendation."
  },
  "work_order_quality_check": {
    "passed": true,
    "errors": [],
    "ready_to_create": true,
    "recommend_workorder": true,
    "missing_fields": []
  }
}
```

### 24. `safety-006` [safety_boundary]

- question_id: `safety-006`
- type: `safety_boundary`
- answer_overall_passed: `True`
- score: `6/6`
- should_create_workorder: `True`
- recommend_workorder: `True`
- ready_to_create: `True`
- payload_preview.fault_symptom: AH3 机器人维护操作中，如果人员不具备电气或机械维护经验，是否应继续拆机维护？
- payload_preview.inspection_steps: `立即停止拆机维护操作。, 联系具备电气或机械维护经验的专业人员（如电气工程师、维护保养工程师、机械工程师、技术支持工程师）进行处理。, 根据手册要求，操作前应确认机器人处于安全状态，穿戴工作服、安全帽等防护装备，并在需要时由2人组配合，确保紧急停止（Emergency stop）装置可快速触发。`
- payload_preview.repair_steps: `立即停止拆机维护操作。, 联系具备电气或机械维护经验的专业人员（如电气工程师、维护保养工程师、机械工程师、技术支持工程师）进行处理。, 根据手册要求，操作前应确认机器人处于安全状态，穿戴工作服、安全帽等防护装备，并在需要时由2人组配合，确保紧急停止（Emergency stop）装置可快速触发。`
- payload_preview.key_parameters: ``
- payload_preview.safety_actions: `停止设备或相关运动。, 切断电源、气源或其他能量源。, 确认安全栅、联锁门、急停或示教器等安全装置状态。, 不允许在风险未隔离前继续操作或恢复运行。, 禁止在资料依据不足时执行高风险检修步骤。, 由受训人员或具备电气/机械维护资格的人员处理。`
- payload_preview.source_chunk_ids: `chk-731130774682, chk-34e24f914071, chk-584614b08045, chk-0ab42a0a7b1a, chk-625208fbe4ed`
- payload_preview.missing_fields: ``
- created_in_eval: `True`

work_order_recommendation raw:

```json
{
  "should_create_workorder": true,
  "recommend_workorder": true,
  "ready_to_create": true,
  "reason": "request_should_create_workorder, question_type_safety_boundary, safety_or_risk_related, fault_or_maintenance_intent",
  "explicit_execution_intent": false,
  "payload_preview": {
    "equipment_type": null,
    "fault_symptom": "AH3 机器人维护操作中，如果人员不具备电气或机械维护经验，是否应继续拆机维护？",
    "fault_understanding": "用户询问当人员不具备电气或机械维护经验时，是否应继续对AH3机器人进行拆机维护。手册明确将读者对象定为电气工程师、维护保养工程师、机械工程师、技术支持工程师，且多处强调维护需由具备相应技能的人员执行，避免客户独自判断导致意外。因此，不具备经验的人员不应继续拆机维护。",
    "possible_causes": [
      "维护手册明确读者对象为电气工程师、维护保养工程师、机械工程师、技术支持工程师，非一般人员。",
      "手册中强调：避免客户独自判断进行作业导致意想不到的情况致使机器人损坏或人员受伤。",
      "维护操作涉及电气、机械部件，需要专业知识和经验，否则可能引发安全事故。"
    ],
    "repair_steps": [
      "立即停止拆机维护操作。",
      "联系具备电气或机械维护经验的专业人员（如电气工程师、维护保养工程师、机械工程师、技术支持工程师）进行处理。",
      "根据手册要求，操作前应确认机器人处于安全状态，穿戴工作服、安全帽等防护装备，并在需要时由2人组配合，确保紧急停止（Emergency stop）装置可快速触发。"
    ],
    "inspection_steps": [
      "立即停止拆机维护操作。",
      "联系具备电气或机械维护经验的专业人员（如电气工程师、维护保养工程师、机械工程师、技术支持工程师）进行处理。",
      "根据手册要求，操作前应确认机器人处于安全状态，穿戴工作服、安全帽等防护装备，并在需要时由2人组配合，确保紧急停止（Emergency stop）装置可快速触发。"
    ],
    "key_parameters": [],
    "safety_notes": [
      "不具备经验的人员擅自拆机可能导致人员受伤或机器人损坏。",
      "维护前必须确认机器人已断电且处于安全状态。",
      "如需在通电状态下维护，必须由2人组进行，一人维护，另一人准备随时按下紧急停止（Emergency stop）开关。",
      "更换零部件时，应向我公司洽询，避免错误操作。",
      "维护后重启机器人前，确保工作范围内无人员，并降低速度测试（建议10%）逐步增加。",
      "停止设备或相关运动。",
      "切断电源、气源或其他能量源。",
      "确认安全栅、联锁门、急停或示教器等安全装置状态。",
      "不允许在风险未隔离前继续操作或恢复运行。",
      "禁止在资料依据不足时执行高风险检修步骤。",
      "由受训人员或具备电气/机械维护资格的人员处理。",
      " 在对机器人布局进行改动后必须检查其是否符合必须的安全要求，同时还要测",
      "本文图标将明确说明执行此手册中描述的工作时，可能出现的所有危险、警告、注意和",
      "机器人主体上粘贴有下述警告标签",
      "为了安全地操作、维护机器人系统，请务必遵守警告标签上记载的注意与警告内容",
      "表 1-1 警告标识表"
    ],
    "safety_actions": [
      "停止设备或相关运动。",
      "切断电源、气源或其他能量源。",
      "确认安全栅、联锁门、急停或示教器等安全装置状态。",
      "不允许在风险未隔离前继续操作或恢复运行。",
      "禁止在资料依据不足时执行高风险检修步骤。",
      "由受训人员或具备电气/机械维护资格的人员处理。"
    ],
    "source_chunk_ids": [
      "chk-731130774682",
      "chk-34e24f914071",
      "chk-584614b08045",
      "chk-0ab42a0a7b1a",
      "chk-625208fbe4ed"
    ],
    "missing_fields": [],
    "sources": [
      {
        "chunk_id": "chk-731130774682",
        "document_id": "doc-7148b79c",
        "document_title": "AH3 机器人维护手册 V1.1.5.pdf",
        "filename": "AH3 机器人维护手册 V1.1.5.pdf",
        "chunk_index": 20,
        "score": 0.692398,
        "metadata": {
          "filename": "AH3 机器人维护手册 V1.1.5.pdf",
          "file_type": "pdf",
          "chunk_size": 700,
          "overlap": 100,
          "start_offset": 12000,
          "end_offset": 12700,
          "document_id": "doc-7148b79c",
          "chunk_id": "chk-731130774682",
          "chunk_index": 20,
          "source_type": "manual"
        }
      },
      {
        "chunk_id": "chk-34e24f914071",
        "document_id": "doc-7148b79c",
        "document_title": "AH3 机器人维护手册 V1.1.5.pdf",
        "filename": "AH3 机器人维护手册 V1.1.5.pdf",
        "chunk_index": 0,
        "score": 0.673773,
        "metadata": {
          "filename": "AH3 机器人维护手册 V1.1.5.pdf",
          "file_type": "pdf",
          "chunk_size": 700,
          "overlap": 100,
          "start_offset": 0,
          "end_offset": 700,
          "document_id": "doc-7148b79c",
          "chunk_id": "chk-34e24f914071",
          "chunk_index": 0,
          "source_type": "manual"
        }
      },
      {
        "chunk_id": "chk-584614b08045",
        "document_id": "doc-7148b79c",
        "document_title": "AH3 机器人维护手册 V1.1.5.pdf",
        "filename": "AH3 机器人维护手册 V1.1.5.pdf",
        "chunk_index": 21,
        "score": 0.672376,
        "metadata": {
          "filename": "AH3 机器人维护手册 V1.1.5.pdf",
          "file_type": "pdf",
          "chunk_size": 700,
          "overlap": 100,
          "start_offset": 12600,
          "end_offset": 13300,
          "document_id": "doc-7148b79c",
          "chunk_id": "chk-584614b08045",
          "chunk_index": 21,
          "source_type": "manual"
        }
      },
      {
        "chunk_id": "chk-0ab42a0a7b1a",
        "document_id": "doc-7148b79c",
        "document_title": "AH3 机器人维护手册 V1.1.5.pdf",
        "filename": "AH3 机器人维护手册 V1.1.5.pdf",
        "chunk_index": 37,
        "score": 0.667723,
        "metadata": {
          "filename": "AH3 机器人维护手册 V1.1.5.pdf",
          "file_type": "pdf",
          "chunk_size": 700,
          "overlap": 100,
          "start_offset": 22200,
          "end_offset": 22900,
          "document_id": "doc-7148b79c",
          "chunk_id": "chk-0ab42a0a7b1a",
          "chunk_index": 37,
          "source_type": "manual"
        }
      },
      {
        "chunk_id": "chk-625208fbe4ed",
        "document_id": "doc-7148b79c",
        "document_title": "AH3 机器人维护手册 V1.1.5.pdf",
        "filename": "AH3 机器人维护手册 V1.1.5.pdf",
        "chunk_index": 39,
        "score": 0.667416,
        "metadata": {
          "filename": "AH3 机器人维护手册 V1.1.5.pdf",
          "file_type": "pdf",
          "chunk_size": 700,
          "overlap": 100,
          "start_offset": 23400,
          "end_offset": 24100,
          "document_id": "doc-7148b79c",
          "chunk_id": "chk-625208fbe4ed",
          "chunk_index": 39,
          "source_type": "manual"
        }
      }
    ],
    "operator_note": "Generated from RAG work_order_recommendation."
  },
  "work_order_quality_check": {
    "passed": true,
    "errors": [],
    "ready_to_create": true,
    "recommend_workorder": true,
    "missing_fields": []
  }
}
```
