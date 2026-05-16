# Real Industry RAG Eval Detailed Report v0.2.0

- generated_at: `2026-05-16 12:05:58`
- source_report: `data/demo/real_industry_eval_report.md`
- baseline_report: `data/demo/real_industry_eval_report_baseline_before_v0.2.0.md`
- scope: `24 题真实工业 RAG 评测诊断，不包含 P0 功能改动`

## 汇总统计

- repair 触发次数: `11`
- safety guard 触发次数: `20`
- industrial term preserve 触发次数: `10`
- work_order_recommendation 触发次数: `23`
- 原失败题中靠 repair 修复的题数: `6`
- 原失败题中靠 safety guard 修复的题数: `10`
- 原失败题中靠 term preserve 修复的题数: `6`

> 说明：repair 统计来自 `answer_repair_applied`；safety guard 统计来自 `safety_guard_assessment.is_safety_question`；industrial term preserve 统计来自 `term_check.preserved_terms/missing_preserved_terms`；work_order_recommendation 统计优先使用 `validation.checks.workorder_check.ready_to_create`。

## 逐题诊断

### 01. `smoke-001` [smoke]

- question_id: `smoke-001`
- type: `smoke`
- overall_passed: `True`
- score: `6/6`
- question: 摩托车发动机火花塞应该如何检查和安装？请给出关键间隙和拧紧要求。
- required_keywords: `火花塞, 0.7, 0.9, 20, N·m`
- matched_keywords_before_repair: `火花塞, 0.7, 0.9, 20, N·m`
- missing_keywords_before_repair: ``
- repair_applied: `False`
- matched_keywords_after_repair: `火花塞, 0.7, 0.9, 20, N·m`
- missing_keywords_after_repair: ``

safety_check 详细结果：

```json
{
  "assessment": {
    "is_safety_question": false,
    "trigger_reasons": [],
    "question_safety_terms": [],
    "question_english_safety_terms": [],
    "source_safety_terms": [],
    "risk_keywords": [
      "拆卸",
      "维修",
      "更换"
    ],
    "manual_basis": [
      "所有螺栓安装后，必须使用扭力扳手校验并打紧至规定扭矩",
      "注意：必须测量基圆位置，非凸轮升程段",
      "摩托车发动机维修手册.pdf",
      "，若有损坏或变形，则应更换火花塞",
      "2. 用塞尺测量火花塞间隙 a，超出范围须更换火花塞"
    ]
  },
  "check": {
    "passed": true,
    "errors": [],
    "signal_count": 0,
    "english_terms_missing": []
  }
}
```

term_check 详细结果：

```json
{
  "passed": true,
  "preserved_terms": [],
  "missing_preserved_terms": [],
  "checked_text_length": 1273
}
```

work_order_recommendation：

```json
{
  "ready_to_create": true,
  "reason": "validation.workorder_check.ready_to_create=True",
  "payload_preview": {
    "fault_symptom": "摩托车发动机火花塞应该如何检查和安装？请给出关键间隙和拧紧要求。",
    "repair_steps": [],
    "safety_actions": [],
    "source_chunk_ids": [
      "chk-21541424d16a",
      "chk-b91af999fdd1",
      "chk-4d7f935536ae",
      "chk-dfb84876691d",
      "chk-ab08fbdb930b"
    ]
  },
  "created_in_eval": false,
  "work_order_id": "",
  "raw_report_included": false,
  "note": "原始评测报告未直接打印完整 work_order_recommendation，本节由 question、validation.workorder_check、sources 诊断重建。"
}
```

Top-5 sources：

- Top 1: filename=`摩托车发动机维修手册.pdf` | chunk_id=`chk-21541424d16a` | chunk_index=`2` | score=`0.798056`
- Top 2: filename=`摩托车发动机维修手册.pdf` | chunk_id=`chk-b91af999fdd1` | chunk_index=`1` | score=`0.714229`
- Top 3: filename=`摩托车发动机维修手册.pdf` | chunk_id=`chk-4d7f935536ae` | chunk_index=`13` | score=`0.697461`
- Top 4: filename=`摩托车发动机维修手册.pdf` | chunk_id=`chk-dfb84876691d` | chunk_index=`5` | score=`0.692629`
- Top 5: filename=`摩托车发动机维修手册.pdf` | chunk_id=`chk-ab08fbdb930b` | chunk_index=`9` | score=`0.688442`

### 02. `smoke-002` [smoke]

- question_id: `smoke-002`
- type: `smoke`
- overall_passed: `True`
- score: `6/6`
- question: AH3 机器人维护手册主要面向哪些维护内容？日常维护时应关注哪些安全提示？
- required_keywords: `AH3, 维护, 安全, 检查`
- matched_keywords_before_repair: `AH3, 维护, 安全, 检查`
- missing_keywords_before_repair: ``
- repair_applied: `False`
- matched_keywords_after_repair: `AH3, 维护, 安全, 检查`
- missing_keywords_after_repair: ``

safety_check 详细结果：

```json
{
  "assessment": {
    "is_safety_question": true,
    "trigger_reasons": [
      "must_have_safety",
      "question_safety_terms"
    ],
    "question_safety_terms": [
      "维护"
    ],
    "question_english_safety_terms": [],
    "source_safety_terms": [],
    "risk_keywords": [
      "维护"
    ],
    "manual_basis": [
      "本文图标将明确说明执行此手册中描述的工作时，可能出现的所有危险、警告、注意和",
      "机器人主体上粘贴有下述警告标签",
      "为了安全地操作、维护机器人系统，请务必遵守警告标签上记载的注意与警告内容",
      "表 1-1 警告标识表",
      "禁止拆解，避免发"
    ]
  },
  "check": {
    "passed": true,
    "errors": [],
    "signal_count": 8,
    "english_terms_missing": []
  }
}
```

term_check 详细结果：

```json
{
  "passed": true,
  "preserved_terms": [
    "Emergency stop"
  ],
  "missing_preserved_terms": [],
  "checked_text_length": 2170
}
```

work_order_recommendation：

```json
{
  "ready_to_create": true,
  "reason": "safety_guard.is_safety_question=True; validation.workorder_check.ready_to_create=True",
  "payload_preview": {
    "fault_symptom": "AH3 机器人维护手册主要面向哪些维护内容？日常维护时应关注哪些安全提示？",
    "repair_steps": [],
    "safety_actions": [
      "停止设备或相关运动",
      "切断电源、气源或其他能量源",
      "确认安全装置状态并由受训人员处理"
    ],
    "source_chunk_ids": [
      "chk-34e24f914071",
      "chk-584614b08045",
      "chk-f836f9d469f8",
      "chk-7d795b762e99",
      "chk-a9523db152cf"
    ]
  },
  "created_in_eval": false,
  "work_order_id": "",
  "raw_report_included": false,
  "note": "原始评测报告未直接打印完整 work_order_recommendation，本节由 question、validation.workorder_check、sources 诊断重建。"
}
```

Top-5 sources：

- Top 1: filename=`AH3 机器人维护手册 V1.1.5.pdf` | chunk_id=`chk-34e24f914071` | chunk_index=`0` | score=`0.816121`
- Top 2: filename=`AH3 机器人维护手册 V1.1.5.pdf` | chunk_id=`chk-584614b08045` | chunk_index=`21` | score=`0.746096`
- Top 3: filename=`AH3 机器人维护手册 V1.1.5.pdf` | chunk_id=`chk-f836f9d469f8` | chunk_index=`15` | score=`0.73096`
- Top 4: filename=`AH3 机器人维护手册 V1.1.5.pdf` | chunk_id=`chk-7d795b762e99` | chunk_index=`4` | score=`0.72899`
- Top 5: filename=`AH3 机器人维护手册 V1.1.5.pdf` | chunk_id=`chk-a9523db152cf` | chunk_index=`22` | score=`0.726166`

### 03. `smoke-003` [smoke]

- question_id: `smoke-003`
- type: `smoke`
- overall_passed: `True`
- score: `6/6`
- question: bfp-a3570l 安全手册中的剩余风险地图和剩余风险一览表是用来做什么的？
- required_keywords: `剩余风险, 保护措施, 危险, 警告`
- matched_keywords_before_repair: `剩余风险, 保护措施, 危险, 警告`
- missing_keywords_before_repair: ``
- repair_applied: `True`
- repair_reason: `validation repair_required=true`
- matched_keywords_after_repair: `剩余风险, 保护措施, 危险, 警告`
- missing_keywords_after_repair: ``

safety_check 详细结果：

```json
{
  "assessment": {
    "is_safety_question": true,
    "trigger_reasons": [
      "must_have_safety",
      "safety_manual_source"
    ],
    "question_safety_terms": [],
    "question_english_safety_terms": [],
    "source_safety_terms": [
      "safety manual",
      "bfp-a3570l"
    ],
    "risk_keywords": [
      "拆卸",
      "维护",
      "电源",
      "急停",
      "危险",
      "停止"
    ],
    "manual_basis": [
      "危险",
      "警告",
      "部位 B No.2、3、6、7 危险",
      "而言危险且严酷的场所也可长时间地持续工作",
      "特有危险"
    ]
  },
  "check": {
    "passed": true,
    "errors": [],
    "signal_count": 8,
    "english_terms_missing": []
  }
}
```

term_check 详细结果：

```json
{
  "passed": true,
  "preserved_terms": [
    "Emergency stop"
  ],
  "missing_preserved_terms": [],
  "checked_text_length": 1900
}
```

work_order_recommendation：

```json
{
  "ready_to_create": true,
  "reason": "safety_guard.is_safety_question=True; validation.workorder_check.ready_to_create=True",
  "payload_preview": {
    "fault_symptom": "bfp-a3570l 安全手册中的剩余风险地图和剩余风险一览表是用来做什么的？",
    "repair_steps": [],
    "safety_actions": [
      "停止设备或相关运动",
      "切断电源、气源或其他能量源",
      "确认安全装置状态并由受训人员处理"
    ],
    "source_chunk_ids": [
      "chk-6d506dc17126",
      "chk-5e0af5c054da",
      "chk-27c9c85ace60",
      "chk-2fa410c18c12",
      "chk-f836f9d469f8"
    ]
  },
  "created_in_eval": false,
  "work_order_id": "",
  "raw_report_included": false,
  "note": "原始评测报告未直接打印完整 work_order_recommendation，本节由 question、validation.workorder_check、sources 诊断重建。"
}
```

Top-5 sources：

- Top 1: filename=`bfp-a3570l.pdf` | chunk_id=`chk-6d506dc17126` | chunk_index=`0` | score=`0.692703`
- Top 2: filename=`bfp-a3570l.pdf` | chunk_id=`chk-5e0af5c054da` | chunk_index=`1` | score=`0.58272`
- Top 3: filename=`bfp-a3570l.pdf` | chunk_id=`chk-27c9c85ace60` | chunk_index=`18` | score=`0.571339`
- Top 4: filename=`safety manual for fanuc educational cell.pdf` | chunk_id=`chk-2fa410c18c12` | chunk_index=`7` | score=`0.567688`
- Top 5: filename=`AH3 机器人维护手册 V1.1.5.pdf` | chunk_id=`chk-f836f9d469f8` | chunk_index=`15` | score=`0.550905`

### 04. `smoke-004` [smoke]

- question_id: `smoke-004`
- type: `smoke`
- overall_passed: `True`
- score: `6/6`
- question: FANUC educational cell 安全手册说明了哪些机器人安全使用注意事项？
- required_keywords: `FANUC, safety, robot, emergency`
- matched_keywords_before_repair: `FANUC, safety, emergency`
- missing_keywords_before_repair: `robot`
- repair_applied: `True`
- repair_reason: `keyword_missing: robot`
- matched_keywords_after_repair: `FANUC, safety, robot, emergency`
- missing_keywords_after_repair: ``

safety_check 详细结果：

```json
{
  "assessment": {
    "is_safety_question": true,
    "trigger_reasons": [
      "must_have_safety",
      "safety_manual_source"
    ],
    "question_safety_terms": [],
    "question_english_safety_terms": [],
    "source_safety_terms": [
      "safety manual",
      "bfp-a3570l"
    ],
    "risk_keywords": [
      "维护",
      "危险",
      "禁止",
      "safety fence",
      "emergency stop",
      "stop"
    ],
    "manual_basis": [
      "on safety with \"Warning\" or \"Caution\" according to its severit",
      "危险",
      "observe the work being performed. If any danger arises, the user should be ready to press the",
      "· 禁止未经允许转载本手册的部分或全部内容",
      "To ensure the safety of workers and prevent damage to the machine, this manual indicates each precaution"
    ]
  },
  "check": {
    "passed": true,
    "errors": [],
    "signal_count": 8,
    "english_terms_missing": []
  }
}
```

term_check 详细结果：

```json
{
  "passed": true,
  "preserved_terms": [
    "Emergency stop",
    "safety fence"
  ],
  "missing_preserved_terms": [],
  "checked_text_length": 3424
}
```

work_order_recommendation：

```json
{
  "ready_to_create": true,
  "reason": "safety_guard.is_safety_question=True; validation.workorder_check.ready_to_create=True",
  "payload_preview": {
    "fault_symptom": "FANUC educational cell 安全手册说明了哪些机器人安全使用注意事项？",
    "repair_steps": [],
    "safety_actions": [
      "停止设备或相关运动",
      "切断电源、气源或其他能量源",
      "确认安全装置状态并由受训人员处理"
    ],
    "source_chunk_ids": [
      "chk-c16663488d97",
      "chk-5e0af5c054da",
      "chk-9b93b9d6895c",
      "chk-877bfd5c9b10",
      "chk-6a6965a98897"
    ]
  },
  "created_in_eval": false,
  "work_order_id": "",
  "raw_report_included": false,
  "note": "原始评测报告未直接打印完整 work_order_recommendation，本节由 question、validation.workorder_check、sources 诊断重建。"
}
```

Top-5 sources：

- Top 1: filename=`safety manual for fanuc educational cell.pdf` | chunk_id=`chk-c16663488d97` | chunk_index=`5` | score=`0.699092`
- Top 2: filename=`bfp-a3570l.pdf` | chunk_id=`chk-5e0af5c054da` | chunk_index=`1` | score=`0.683044`
- Top 3: filename=`safety manual for fanuc educational cell.pdf` | chunk_id=`chk-9b93b9d6895c` | chunk_index=`27` | score=`0.672677`
- Top 4: filename=`safety manual for fanuc educational cell.pdf` | chunk_id=`chk-877bfd5c9b10` | chunk_index=`150` | score=`0.671748`
- Top 5: filename=`bfp-a3570l.pdf` | chunk_id=`chk-6a6965a98897` | chunk_index=`19` | score=`0.665423`

### 05. `smoke-005` [smoke]

- question_id: `smoke-005`
- type: `smoke`
- overall_passed: `True`
- score: `6/6`
- question: CM2x-OM0230Q 气缸手册包含哪些主要章节？
- required_keywords: `气缸, 产品规格, 设置方法, 保养点检`
- matched_keywords_before_repair: `气缸, 产品规格, 设置方法, 保养点检`
- missing_keywords_before_repair: ``
- repair_applied: `False`
- matched_keywords_after_repair: `气缸, 产品规格, 设置方法, 保养点检`
- missing_keywords_after_repair: ``

safety_check 详细结果：

```json
{
  "assessment": {
    "is_safety_question": false,
    "trigger_reasons": [],
    "question_safety_terms": [],
    "question_english_safety_terms": [],
    "source_safety_terms": [],
    "risk_keywords": [
      "维修",
      "更换",
      "气源",
      "危险"
    ],
    "manual_basis": [
      "这些注意事项，按照危害和损伤的大小及紧急程度分为「注意」 「警告」 「危险」三个等级",
      "安全注意事项 P2",
      "2-2. 设计注意事项",
      "3-1. 活塞杆密封圈的更换方法",
      "安全注意事项"
    ]
  },
  "check": {
    "passed": true,
    "errors": [],
    "signal_count": 0,
    "english_terms_missing": []
  }
}
```

term_check 详细结果：

```json
{
  "passed": true,
  "preserved_terms": [],
  "missing_preserved_terms": [],
  "checked_text_length": 813
}
```

work_order_recommendation：

```json
{
  "ready_to_create": false,
  "reason": "validation.workorder_check.ready_to_create=False",
  "payload_preview": {
    "fault_symptom": "CM2x-OM0230Q 气缸手册包含哪些主要章节？",
    "repair_steps": [],
    "safety_actions": [],
    "source_chunk_ids": [
      "chk-65d6cca0f77c",
      "chk-144fe11aea33",
      "chk-d185bce0f648",
      "chk-44ce5ae9159a",
      "chk-763a8cf76e61"
    ]
  },
  "created_in_eval": false,
  "work_order_id": "",
  "raw_report_included": false,
  "note": "原始评测报告未直接打印完整 work_order_recommendation，本节由 question、validation.workorder_check、sources 诊断重建。"
}
```

Top-5 sources：

- Top 1: filename=`CM2x-OM0230Q.pdf` | chunk_id=`chk-65d6cca0f77c` | chunk_index=`0` | score=`0.676752`
- Top 2: filename=`CG1x-OM0006N.pdf` | chunk_id=`chk-144fe11aea33` | chunk_index=`0` | score=`0.616203`
- Top 3: filename=`CG1x-OM0006N.pdf` | chunk_id=`chk-d185bce0f648` | chunk_index=`0` | score=`0.61618`
- Top 4: filename=`CG1x-OM0006N.pdf` | chunk_id=`chk-44ce5ae9159a` | chunk_index=`27` | score=`0.556921`
- Top 5: filename=`CG1x-OM0006N.pdf` | chunk_id=`chk-763a8cf76e61` | chunk_index=`27` | score=`0.556921`

### 06. `smoke-006` [smoke]

- question_id: `smoke-006`
- type: `smoke`
- overall_passed: `True`
- score: `6/6`
- question: CG1x-OM0006N 不锈钢气缸手册包含哪些维修保养和故障对策内容？
- required_keywords: `不锈钢气缸, 维修保养, 点检, 故障`
- matched_keywords_before_repair: `维修保养, 点检, 故障`
- missing_keywords_before_repair: `不锈钢气缸`
- repair_applied: `True`
- repair_reason: `keyword_missing: 不锈钢气缸`
- matched_keywords_after_repair: `不锈钢气缸, 维修保养, 点检, 故障`
- missing_keywords_after_repair: ``

safety_check 详细结果：

```json
{
  "assessment": {
    "is_safety_question": true,
    "trigger_reasons": [
      "question_safety_terms"
    ],
    "question_safety_terms": [
      "维修"
    ],
    "question_english_safety_terms": [],
    "source_safety_terms": [],
    "risk_keywords": [
      "维修"
    ],
    "manual_basis": [
      "这些注意事项，按照危害和损伤的大小及紧急程度分为「注意」 「警告」 「危险」三个等级",
      "安全注意事项 P2",
      "产品个别注意事项 P4",
      "2-2.设计注意事项",
      "3.维修保养 P16"
    ]
  },
  "check": {
    "passed": true,
    "errors": [],
    "signal_count": 8,
    "english_terms_missing": []
  }
}
```

term_check 详细结果：

```json
{
  "passed": true,
  "preserved_terms": [],
  "missing_preserved_terms": [],
  "checked_text_length": 1211
}
```

work_order_recommendation：

```json
{
  "ready_to_create": true,
  "reason": "safety_guard.is_safety_question=True; validation.workorder_check.ready_to_create=True",
  "payload_preview": {
    "fault_symptom": "CG1x-OM0006N 不锈钢气缸手册包含哪些维修保养和故障对策内容？",
    "repair_steps": [],
    "safety_actions": [
      "停止设备或相关运动",
      "切断电源、气源或其他能量源",
      "确认安全装置状态并由受训人员处理"
    ],
    "source_chunk_ids": [
      "chk-144fe11aea33",
      "chk-d185bce0f648",
      "chk-65d6cca0f77c",
      "chk-44ce5ae9159a",
      "chk-763a8cf76e61"
    ]
  },
  "created_in_eval": false,
  "work_order_id": "",
  "raw_report_included": false,
  "note": "原始评测报告未直接打印完整 work_order_recommendation，本节由 question、validation.workorder_check、sources 诊断重建。"
}
```

Top-5 sources：

- Top 1: filename=`CG1x-OM0006N.pdf` | chunk_id=`chk-144fe11aea33` | chunk_index=`0` | score=`0.730002`
- Top 2: filename=`CG1x-OM0006N.pdf` | chunk_id=`chk-d185bce0f648` | chunk_index=`0` | score=`0.729974`
- Top 3: filename=`CM2x-OM0230Q.pdf` | chunk_id=`chk-65d6cca0f77c` | chunk_index=`0` | score=`0.664283`
- Top 4: filename=`CG1x-OM0006N.pdf` | chunk_id=`chk-44ce5ae9159a` | chunk_index=`27` | score=`0.611462`
- Top 5: filename=`CG1x-OM0006N.pdf` | chunk_id=`chk-763a8cf76e61` | chunk_index=`27` | score=`0.611462`

### 07. `param-001` [parameter]

- question_id: `param-001`
- type: `parameter`
- overall_passed: `True`
- score: `6/6`
- question: 摩托车发动机火花塞间隙标准值是多少？安装火花塞的拧紧力矩是多少？
- required_keywords: `0.7, 0.9, 20, N·m`
- matched_keywords_before_repair: `0.7, 0.9, 20, N·m`
- missing_keywords_before_repair: ``
- repair_applied: `False`
- matched_keywords_after_repair: `0.7, 0.9, 20, N·m`
- missing_keywords_after_repair: ``

safety_check 详细结果：

```json
{
  "assessment": {
    "is_safety_question": false,
    "trigger_reasons": [],
    "question_safety_terms": [],
    "question_english_safety_terms": [],
    "source_safety_terms": [],
    "risk_keywords": [
      "拆卸",
      "维修",
      "更换"
    ],
    "manual_basis": [
      "所有螺栓安装后，必须使用扭力扳手校验并打紧至规定扭矩",
      "注意：必须测量基圆位置，非凸轮升程段",
      "摩托车发动机维修手册.pdf",
      "，若有损坏或变形，则应更换火花塞",
      "2. 用塞尺测量火花塞间隙 a，超出范围须更换火花塞"
    ]
  },
  "check": {
    "passed": true,
    "errors": [],
    "signal_count": 0,
    "english_terms_missing": []
  }
}
```

term_check 详细结果：

```json
{
  "passed": true,
  "preserved_terms": [],
  "missing_preserved_terms": [],
  "checked_text_length": 892
}
```

work_order_recommendation：

```json
{
  "ready_to_create": true,
  "reason": "validation.workorder_check.ready_to_create=True",
  "payload_preview": {
    "fault_symptom": "摩托车发动机火花塞间隙标准值是多少？安装火花塞的拧紧力矩是多少？",
    "repair_steps": [],
    "safety_actions": [],
    "source_chunk_ids": [
      "chk-21541424d16a",
      "chk-d026f9ac3955",
      "chk-dfb84876691d",
      "chk-4d7f935536ae",
      "chk-ab08fbdb930b"
    ]
  },
  "created_in_eval": false,
  "work_order_id": "",
  "raw_report_included": false,
  "note": "原始评测报告未直接打印完整 work_order_recommendation，本节由 question、validation.workorder_check、sources 诊断重建。"
}
```

Top-5 sources：

- Top 1: filename=`摩托车发动机维修手册.pdf` | chunk_id=`chk-21541424d16a` | chunk_index=`2` | score=`0.747561`
- Top 2: filename=`摩托车发动机维修手册.pdf` | chunk_id=`chk-d026f9ac3955` | chunk_index=`6` | score=`0.653299`
- Top 3: filename=`摩托车发动机维修手册.pdf` | chunk_id=`chk-dfb84876691d` | chunk_index=`5` | score=`0.634031`
- Top 4: filename=`摩托车发动机维修手册.pdf` | chunk_id=`chk-4d7f935536ae` | chunk_index=`13` | score=`0.632085`
- Top 5: filename=`摩托车发动机维修手册.pdf` | chunk_id=`chk-ab08fbdb930b` | chunk_index=`9` | score=`0.631945`

### 08. `param-002` [parameter]

- question_id: `param-002`
- type: `parameter`
- overall_passed: `True`
- score: `6/6`
- question: 摩托车发动机测量压缩压力时，标准压缩压力范围是多少？
- required_keywords: `1300, 1900, 500, 900, kPa`
- matched_keywords_before_repair: ``
- missing_keywords_before_repair: `1300, 1900, 500, 900, kPa`
- repair_applied: `True`
- repair_reason: `keyword_missing: 1300, 1900, 500, 900, kPa`
- matched_keywords_after_repair: `1300, 1900, 500, 900, kPa`
- missing_keywords_after_repair: ``

safety_check 详细结果：

```json
{
  "assessment": {
    "is_safety_question": true,
    "trigger_reasons": [
      "must_have_safety"
    ],
    "question_safety_terms": [],
    "question_english_safety_terms": [],
    "source_safety_terms": [],
    "risk_keywords": [
      "拆卸",
      "维修",
      "更换"
    ],
    "manual_basis": [
      "所有螺栓安装后，必须使用扭力扳手校验并打紧至规定扭矩",
      "警告",
      "压缩空气中不得含有化学药品、有机溶剂的合成油、盐分、腐蚀性气体等，以免造成产品破损及",
      "摩托车发动机维修手册.pdf",
      "，若有损坏或变形，则应更换火花塞"
    ]
  },
  "check": {
    "passed": true,
    "errors": [],
    "signal_count": 7,
    "english_terms_missing": []
  }
}
```

term_check 详细结果：

```json
{
  "passed": true,
  "preserved_terms": [],
  "missing_preserved_terms": [],
  "checked_text_length": 1676
}
```

work_order_recommendation：

```json
{
  "ready_to_create": true,
  "reason": "safety_guard.is_safety_question=True; validation.workorder_check.ready_to_create=True",
  "payload_preview": {
    "fault_symptom": "摩托车发动机测量压缩压力时，标准压缩压力范围是多少？",
    "repair_steps": [],
    "safety_actions": [
      "停止设备或相关运动",
      "切断电源、气源或其他能量源",
      "确认安全装置状态并由受训人员处理"
    ],
    "source_chunk_ids": [
      "chk-21541424d16a",
      "chk-d026f9ac3955",
      "chk-dfb84876691d",
      "chk-4896a18d171f",
      "chk-724a5de67b0b"
    ]
  },
  "created_in_eval": false,
  "work_order_id": "",
  "raw_report_included": false,
  "note": "原始评测报告未直接打印完整 work_order_recommendation，本节由 question、validation.workorder_check、sources 诊断重建。"
}
```

Top-5 sources：

- Top 1: filename=`摩托车发动机维修手册.pdf` | chunk_id=`chk-21541424d16a` | chunk_index=`2` | score=`0.687767`
- Top 2: filename=`摩托车发动机维修手册.pdf` | chunk_id=`chk-d026f9ac3955` | chunk_index=`6` | score=`0.621322`
- Top 3: filename=`摩托车发动机维修手册.pdf` | chunk_id=`chk-dfb84876691d` | chunk_index=`5` | score=`0.610289`
- Top 4: filename=`CG1x-OM0006N.pdf` | chunk_id=`chk-4896a18d171f` | chunk_index=`8` | score=`0.602476`
- Top 5: filename=`CG1x-OM0006N.pdf` | chunk_id=`chk-724a5de67b0b` | chunk_index=`8` | score=`0.602476`

### 09. `param-003` [parameter]

- question_id: `param-003`
- type: `parameter`
- overall_passed: `True`
- score: `6/6`
- question: CM2 系列气缸使用前需要确认哪些空气源和速度控制相关条件？
- required_keywords: `使用空气, 速度控制, 气缸, 调整`
- matched_keywords_before_repair: `速度控制, 气缸, 调整`
- missing_keywords_before_repair: `使用空气`
- repair_applied: `True`
- repair_reason: `keyword_missing: 使用空气`
- matched_keywords_after_repair: `使用空气, 速度控制, 气缸, 调整`
- missing_keywords_after_repair: ``

safety_check 详细结果：

```json
{
  "assessment": {
    "is_safety_question": true,
    "trigger_reasons": [
      "question_safety_terms"
    ],
    "question_safety_terms": [
      "气源"
    ],
    "question_english_safety_terms": [],
    "source_safety_terms": [],
    "risk_keywords": [
      "气源"
    ],
    "manual_basis": [
      "这种情况必须十分注意",
      "警告",
      "安全注意事项 P2",
      "2-2. 设计注意事项",
      "3-1. 活塞杆密封圈的更换方法"
    ]
  },
  "check": {
    "passed": true,
    "errors": [],
    "signal_count": 7,
    "english_terms_missing": []
  }
}
```

term_check 详细结果：

```json
{
  "passed": true,
  "preserved_terms": [],
  "missing_preserved_terms": [],
  "checked_text_length": 3750
}
```

work_order_recommendation：

```json
{
  "ready_to_create": true,
  "reason": "safety_guard.is_safety_question=True; validation.workorder_check.ready_to_create=True",
  "payload_preview": {
    "fault_symptom": "CM2 系列气缸使用前需要确认哪些空气源和速度控制相关条件？",
    "repair_steps": [],
    "safety_actions": [
      "停止设备或相关运动",
      "切断电源、气源或其他能量源",
      "确认安全装置状态并由受训人员处理"
    ],
    "source_chunk_ids": [
      "chk-65d6cca0f77c",
      "chk-8bb7d4bc9b80",
      "chk-647729f3f513",
      "chk-730b481cb2cb",
      "chk-bcaa8d1cf42c"
    ]
  },
  "created_in_eval": false,
  "work_order_id": "",
  "raw_report_included": false,
  "note": "原始评测报告未直接打印完整 work_order_recommendation，本节由 question、validation.workorder_check、sources 诊断重建。"
}
```

Top-5 sources：

- Top 1: filename=`CM2x-OM0230Q.pdf` | chunk_id=`chk-65d6cca0f77c` | chunk_index=`0` | score=`0.669675`
- Top 2: filename=`CG1x-OM0006N.pdf` | chunk_id=`chk-8bb7d4bc9b80` | chunk_index=`14` | score=`0.623545`
- Top 3: filename=`CG1x-OM0006N.pdf` | chunk_id=`chk-647729f3f513` | chunk_index=`14` | score=`0.623545`
- Top 4: filename=`CG1x-OM0006N.pdf` | chunk_id=`chk-730b481cb2cb` | chunk_index=`15` | score=`0.619911`
- Top 5: filename=`CG1x-OM0006N.pdf` | chunk_id=`chk-bcaa8d1cf42c` | chunk_index=`15` | score=`0.619911`

### 10. `param-004` [parameter]

- question_id: `param-004`
- type: `parameter`
- overall_passed: `True`
- score: `6/6`
- question: CG1 系列不锈钢气缸磁性开关安装时，安装螺钉的紧固力矩要求是什么？
- required_keywords: `磁性开关, M4, 1, 1.2, N`
- matched_keywords_before_repair: `磁性开关, M4, 1, 1.2, N`
- missing_keywords_before_repair: ``
- repair_applied: `False`
- matched_keywords_after_repair: `磁性开关, M4, 1, 1.2, N`
- missing_keywords_after_repair: ``

safety_check 详细结果：

```json
{
  "assessment": {
    "is_safety_question": false,
    "trigger_reasons": [],
    "question_safety_terms": [],
    "question_english_safety_terms": [],
    "source_safety_terms": [],
    "risk_keywords": [
      "拆卸",
      "维修",
      "维护",
      "更换",
      "气源",
      "电源",
      "危险",
      "停止"
    ],
    "manual_basis": [
      "警告",
      "压缩空气若被误操作会很危险，所以在遵守产品规格的同时，请由对空气压元件有足够知识和",
      "3. 维修保养",
      "1）按上述项目对气缸进行维修保养",
      "2）维护作业"
    ]
  },
  "check": {
    "passed": true,
    "errors": [],
    "signal_count": 0,
    "english_terms_missing": []
  }
}
```

term_check 详细结果：

```json
{
  "passed": true,
  "preserved_terms": [],
  "missing_preserved_terms": [],
  "checked_text_length": 535
}
```

work_order_recommendation：

```json
{
  "ready_to_create": true,
  "reason": "validation.workorder_check.ready_to_create=True",
  "payload_preview": {
    "fault_symptom": "CG1 系列不锈钢气缸磁性开关安装时，安装螺钉的紧固力矩要求是什么？",
    "repair_steps": [],
    "safety_actions": [],
    "source_chunk_ids": [
      "chk-c1f980dc39dd",
      "chk-e3133442503d",
      "chk-a22f19291795",
      "chk-65a4ebe4d849",
      "chk-2fdc017d9509"
    ]
  },
  "created_in_eval": false,
  "work_order_id": "",
  "raw_report_included": false,
  "note": "原始评测报告未直接打印完整 work_order_recommendation，本节由 question、validation.workorder_check、sources 诊断重建。"
}
```

Top-5 sources：

- Top 1: filename=`CG1x-OM0006N.pdf` | chunk_id=`chk-c1f980dc39dd` | chunk_index=`19` | score=`0.701549`
- Top 2: filename=`CG1x-OM0006N.pdf` | chunk_id=`chk-e3133442503d` | chunk_index=`19` | score=`0.701549`
- Top 3: filename=`CM2x-OM0230Q.pdf` | chunk_id=`chk-a22f19291795` | chunk_index=`11` | score=`0.677918`
- Top 4: filename=`CG1x-OM0006N.pdf` | chunk_id=`chk-65a4ebe4d849` | chunk_index=`18` | score=`0.670753`
- Top 5: filename=`CG1x-OM0006N.pdf` | chunk_id=`chk-2fdc017d9509` | chunk_index=`18` | score=`0.670753`

### 11. `param-005` [parameter]

- question_id: `param-005`
- type: `parameter`
- overall_passed: `True`
- score: `6/6`
- question: FANUC 机器人控制器相关安全功能中，Emergency stop、mode select switch、deadman switch 分别属于哪些安全控制主题？
- required_keywords: `Emergency stop, mode select, deadman, teach pendant`
- matched_keywords_before_repair: `Emergency stop, mode select, deadman, teach pendant`
- missing_keywords_before_repair: ``
- repair_applied: `True`
- repair_reason: `validation repair_required=true`
- matched_keywords_after_repair: `Emergency stop, mode select, deadman, teach pendant`
- missing_keywords_after_repair: ``

safety_check 详细结果：

```json
{
  "assessment": {
    "is_safety_question": true,
    "trigger_reasons": [
      "must_have_safety",
      "question_english_safety_terms",
      "safety_manual_source"
    ],
    "question_safety_terms": [],
    "question_english_safety_terms": [
      "emergency stop",
      "deadman switch",
      "stop"
    ],
    "source_safety_terms": [
      "safety manual",
      "bfp-a3570l"
    ],
    "risk_keywords": [
      "emergency stop",
      "deadman switch",
      "stop"
    ],
    "manual_basis": [
      "Based on the risk assessment by FANUC, the number of operations of the deadman switches should not",
      "SRVO-001 Operator panel E-stop Operator panel emergency stop is pressed.",
      "SRVO-002 Teach pendant E-stop Teach pendant emergency stop is pressed.",
      "SRVO-007 External emergency stops External emergency stop input (EES1-EES11, EES2-EES21) is",
      "SRVO-408 DCS SSO Ext Emergency Stop In DCS Safe I/O connect function, SSO[3] is OFF."
    ]
  },
  "check": {
    "passed": true,
    "errors": [],
    "signal_count": 7,
    "english_terms_missing": []
  }
}
```

term_check 详细结果：

```json
{
  "passed": true,
  "preserved_terms": [
    "deadman switch",
    "Emergency stop",
    "interlocking",
    "mode select switch",
    "safety fence",
    "teach pendant"
  ],
  "missing_preserved_terms": [],
  "checked_text_length": 3105
}
```

work_order_recommendation：

```json
{
  "ready_to_create": true,
  "reason": "safety_guard.is_safety_question=True; validation.workorder_check.ready_to_create=True",
  "payload_preview": {
    "fault_symptom": "FANUC 机器人控制器相关安全功能中，Emergency stop、mode select switch、deadman switch 分别属于哪些安全控制主题？",
    "repair_steps": [],
    "safety_actions": [
      "停止设备或相关运动",
      "切断电源、气源或其他能量源",
      "确认安全装置状态并由受训人员处理"
    ],
    "source_chunk_ids": [
      "chk-97c9bf4b7bb0",
      "chk-11932d0c1547",
      "chk-a5646801d304",
      "chk-03d68abdce49",
      "chk-433ca6a8c08f"
    ]
  },
  "created_in_eval": false,
  "work_order_id": "",
  "raw_report_included": false,
  "note": "原始评测报告未直接打印完整 work_order_recommendation，本节由 question、validation.workorder_check、sources 诊断重建。"
}
```

Top-5 sources：

- Top 1: filename=`safety manual for fanuc educational cell.pdf` | chunk_id=`chk-97c9bf4b7bb0` | chunk_index=`105` | score=`0.629936`
- Top 2: filename=`safety manual for fanuc educational cell.pdf` | chunk_id=`chk-11932d0c1547` | chunk_index=`74` | score=`0.608202`
- Top 3: filename=`safety manual for fanuc educational cell.pdf` | chunk_id=`chk-a5646801d304` | chunk_index=`93` | score=`0.589858`
- Top 4: filename=`bfp-a3570l.pdf` | chunk_id=`chk-03d68abdce49` | chunk_index=`37` | score=`0.589603`
- Top 5: filename=`safety manual for fanuc educational cell.pdf` | chunk_id=`chk-433ca6a8c08f` | chunk_index=`61` | score=`0.588695`

### 12. `param-006` [parameter]

- question_id: `param-006`
- type: `parameter`
- overall_passed: `True`
- score: `6/6`
- question: AH3 机器人维护资料中版本号、发布日期和适用对象信息是什么？
- required_keywords: `V1.1.5, 2023-05-15, 维护保养工程师, 机械工程师`
- matched_keywords_before_repair: `V1.1.5`
- missing_keywords_before_repair: `2023-05-15, 维护保养工程师, 机械工程师`
- repair_applied: `True`
- repair_reason: `keyword_missing: 2023-05-15, 维护保养工程师, 机械工程师`
- matched_keywords_after_repair: `V1.1.5, 2023-05-15, 维护保养工程师, 机械工程师`
- missing_keywords_after_repair: ``

safety_check 详细结果：

```json
{
  "assessment": {
    "is_safety_question": true,
    "trigger_reasons": [
      "question_safety_terms"
    ],
    "question_safety_terms": [
      "维护"
    ],
    "question_english_safety_terms": [],
    "source_safety_terms": [],
    "risk_keywords": [
      "维护"
    ],
    "manual_basis": [
      "本文图标将明确说明执行此手册中描述的工作时，可能出现的所有危险、警告、注意和",
      "表 1-1 警告标识表 ........................................................ 5",
      "AH3 机器人维护手册 V1.1.5.pdf",
      "AH3 机器人维护手册",
      "本手册详细描述 AH3 机器人的日常维护保养和安全检查，以及机械、电气零部件的维护"
    ]
  },
  "check": {
    "passed": true,
    "errors": [],
    "signal_count": 8,
    "english_terms_missing": []
  }
}
```

term_check 详细结果：

```json
{
  "passed": true,
  "preserved_terms": [],
  "missing_preserved_terms": [],
  "checked_text_length": 1132
}
```

work_order_recommendation：

```json
{
  "ready_to_create": true,
  "reason": "safety_guard.is_safety_question=True; validation.workorder_check.ready_to_create=True",
  "payload_preview": {
    "fault_symptom": "AH3 机器人维护资料中版本号、发布日期和适用对象信息是什么？",
    "repair_steps": [],
    "safety_actions": [
      "停止设备或相关运动",
      "切断电源、气源或其他能量源",
      "确认安全装置状态并由受训人员处理"
    ],
    "source_chunk_ids": [
      "chk-34e24f914071",
      "chk-7d795b762e99",
      "chk-f836f9d469f8",
      "chk-8b0e4a3e46b4",
      "chk-c382291794e7"
    ]
  },
  "created_in_eval": false,
  "work_order_id": "",
  "raw_report_included": false,
  "note": "原始评测报告未直接打印完整 work_order_recommendation，本节由 question、validation.workorder_check、sources 诊断重建。"
}
```

Top-5 sources：

- Top 1: filename=`AH3 机器人维护手册 V1.1.5.pdf` | chunk_id=`chk-34e24f914071` | chunk_index=`0` | score=`0.772888`
- Top 2: filename=`AH3 机器人维护手册 V1.1.5.pdf` | chunk_id=`chk-7d795b762e99` | chunk_index=`4` | score=`0.7009`
- Top 3: filename=`AH3 机器人维护手册 V1.1.5.pdf` | chunk_id=`chk-f836f9d469f8` | chunk_index=`15` | score=`0.686481`
- Top 4: filename=`AH3 机器人维护手册 V1.1.5.pdf` | chunk_id=`chk-8b0e4a3e46b4` | chunk_index=`2` | score=`0.678943`
- Top 5: filename=`AH3 机器人维护手册 V1.1.5.pdf` | chunk_id=`chk-c382291794e7` | chunk_index=`9` | score=`0.667205`

### 13. `fault-001` [procedure_fault]

- question_id: `fault-001`
- type: `procedure_fault`
- overall_passed: `True`
- score: `6/6`
- question: 摩托车发动机压缩压力低于标准下限时，应该如何判断是活塞环、气缸还是气门相关问题？
- required_keywords: `压缩压力, 机油, 活塞, 气门, 气缸`
- matched_keywords_before_repair: `压缩压力, 机油, 活塞, 气门, 气缸`
- missing_keywords_before_repair: ``
- repair_applied: `False`
- matched_keywords_after_repair: `压缩压力, 机油, 活塞, 气门, 气缸`
- missing_keywords_after_repair: ``

safety_check 详细结果：

```json
{
  "assessment": {
    "is_safety_question": true,
    "trigger_reasons": [
      "must_have_safety"
    ],
    "question_safety_terms": [],
    "question_english_safety_terms": [],
    "source_safety_terms": [],
    "risk_keywords": [
      "拆卸",
      "维修",
      "更换",
      "气源",
      "停止"
    ],
    "manual_basis": [
      "摩托车发动机维修手册.pdf",
      "，若有损坏或变形，则应更换火花塞",
      "2. 用塞尺测量火花塞间隙 a，超出范围须更换火花塞",
      "2. 拆卸火花塞",
      "注意：在拆卸火花塞之前要确保火花塞孔及其周围没有灰尘"
    ]
  },
  "check": {
    "passed": true,
    "errors": [],
    "signal_count": 8,
    "english_terms_missing": []
  }
}
```

term_check 详细结果：

```json
{
  "passed": true,
  "preserved_terms": [],
  "missing_preserved_terms": [],
  "checked_text_length": 2189
}
```

work_order_recommendation：

```json
{
  "ready_to_create": true,
  "reason": "question.should_create_workorder=True; safety_guard.is_safety_question=True; validation.workorder_check.ready_to_create=True",
  "payload_preview": {
    "fault_symptom": "摩托车发动机压缩压力低于标准下限时，应该如何判断是活塞环、气缸还是气门相关问题？",
    "repair_steps": [],
    "safety_actions": [
      "停止设备或相关运动",
      "切断电源、气源或其他能量源",
      "确认安全装置状态并由受训人员处理"
    ],
    "source_chunk_ids": [
      "chk-21541424d16a",
      "chk-3319bc93ff5a",
      "chk-238df46741e0",
      "chk-9bbda50b82bf",
      "chk-f839f9251174"
    ]
  },
  "created_in_eval": true,
  "work_order_id": "wo-3d97460104",
  "raw_report_included": false,
  "note": "原始评测报告未直接打印完整 work_order_recommendation，本节由 question、validation.workorder_check、sources 诊断重建。"
}
```

Top-5 sources：

- Top 1: filename=`摩托车发动机维修手册.pdf` | chunk_id=`chk-21541424d16a` | chunk_index=`2` | score=`0.667088`
- Top 2: filename=`CG1x-OM0006N.pdf` | chunk_id=`chk-3319bc93ff5a` | chunk_index=`24` | score=`0.639796`
- Top 3: filename=`CG1x-OM0006N.pdf` | chunk_id=`chk-238df46741e0` | chunk_index=`24` | score=`0.639796`
- Top 4: filename=`CM2x-OM0230Q.pdf` | chunk_id=`chk-9bbda50b82bf` | chunk_index=`18` | score=`0.636661`
- Top 5: filename=`CG1x-OM0006N.pdf` | chunk_id=`chk-f839f9251174` | chunk_index=`25` | score=`0.626194`

### 14. `fault-002` [procedure_fault]

- question_id: `fault-002`
- type: `procedure_fault`
- overall_passed: `True`
- score: `6/6`
- question: 摩托车起动电机无法正常带动发动机转动时，应按哪些部件和步骤排查？
- required_keywords: `起动电机, 拆卸, 安装, 检查`
- matched_keywords_before_repair: `起动电机, 拆卸, 安装, 检查`
- missing_keywords_before_repair: ``
- repair_applied: `False`
- matched_keywords_after_repair: `起动电机, 拆卸, 安装, 检查`
- missing_keywords_after_repair: ``

safety_check 详细结果：

```json
{
  "assessment": {
    "is_safety_question": true,
    "trigger_reasons": [
      "must_have_safety"
    ],
    "question_safety_terms": [],
    "question_english_safety_terms": [],
    "source_safety_terms": [],
    "risk_keywords": [
      "拆卸",
      "维修",
      "更换"
    ],
    "manual_basis": [
      "警告：不要尝试将弯曲的拨叉轴校直",
      "所有螺栓安装后，必须使用扭力扳手校验并打紧至规定扭矩",
      "摩托车发动机维修手册.pdf",
      "2.2 拆卸起动电机",
      "1. 拆卸涨紧器"
    ]
  },
  "check": {
    "passed": true,
    "errors": [],
    "signal_count": 7,
    "english_terms_missing": []
  }
}
```

term_check 详细结果：

```json
{
  "passed": true,
  "preserved_terms": [],
  "missing_preserved_terms": [],
  "checked_text_length": 2528
}
```

work_order_recommendation：

```json
{
  "ready_to_create": true,
  "reason": "question.should_create_workorder=True; safety_guard.is_safety_question=True; validation.workorder_check.ready_to_create=True",
  "payload_preview": {
    "fault_symptom": "摩托车起动电机无法正常带动发动机转动时，应按哪些部件和步骤排查？",
    "repair_steps": [],
    "safety_actions": [
      "停止设备或相关运动",
      "切断电源、气源或其他能量源",
      "确认安全装置状态并由受训人员处理"
    ],
    "source_chunk_ids": [
      "chk-f33f51c42f12",
      "chk-b91af999fdd1",
      "chk-d5195cfdd53e",
      "chk-dfb84876691d",
      "chk-30c0b27e17aa"
    ]
  },
  "created_in_eval": true,
  "work_order_id": "wo-4fd96f2df2",
  "raw_report_included": false,
  "note": "原始评测报告未直接打印完整 work_order_recommendation，本节由 question、validation.workorder_check、sources 诊断重建。"
}
```

Top-5 sources：

- Top 1: filename=`摩托车发动机维修手册.pdf` | chunk_id=`chk-f33f51c42f12` | chunk_index=`3` | score=`0.738417`
- Top 2: filename=`摩托车发动机维修手册.pdf` | chunk_id=`chk-b91af999fdd1` | chunk_index=`1` | score=`0.672429`
- Top 3: filename=`摩托车发动机维修手册.pdf` | chunk_id=`chk-d5195cfdd53e` | chunk_index=`23` | score=`0.669248`
- Top 4: filename=`摩托车发动机维修手册.pdf` | chunk_id=`chk-dfb84876691d` | chunk_index=`5` | score=`0.665144`
- Top 5: filename=`摩托车发动机维修手册.pdf` | chunk_id=`chk-30c0b27e17aa` | chunk_index=`24` | score=`0.660712`

### 15. `fault-003` [procedure_fault]

- question_id: `fault-003`
- type: `procedure_fault`
- overall_passed: `True`
- score: `6/6`
- question: CG1 不锈钢气缸动作不顺畅、速度变化或行程异常时，应做哪些点检？
- required_keywords: `点检, 作动, 速度, 行程, 安装螺钉`
- matched_keywords_before_repair: `点检, 作动, 速度, 行程`
- missing_keywords_before_repair: `安装螺钉`
- repair_applied: `True`
- repair_reason: `keyword_missing: 安装螺钉`
- matched_keywords_after_repair: `点检, 作动, 速度, 行程, 安装螺钉`
- missing_keywords_after_repair: ``

safety_check 详细结果：

```json
{
  "assessment": {
    "is_safety_question": true,
    "trigger_reasons": [
      "must_have_safety"
    ],
    "question_safety_terms": [],
    "question_english_safety_terms": [],
    "source_safety_terms": [],
    "risk_keywords": [
      "拆卸",
      "维修",
      "更换",
      "气源",
      "危险",
      "停止"
    ],
    "manual_basis": [
      "这些注意事项，按照危害和损伤的大小及紧急程度分为「注意」 「警告」 「危险」三个等级",
      "气源",
      "安全注意事项 P2",
      "产品个别注意事项 P4",
      "2-2.设计注意事项"
    ]
  },
  "check": {
    "passed": true,
    "errors": [],
    "signal_count": 8,
    "english_terms_missing": []
  }
}
```

term_check 详细结果：

```json
{
  "passed": true,
  "preserved_terms": [],
  "missing_preserved_terms": [],
  "checked_text_length": 4187
}
```

work_order_recommendation：

```json
{
  "ready_to_create": true,
  "reason": "question.should_create_workorder=True; safety_guard.is_safety_question=True; validation.workorder_check.ready_to_create=True",
  "payload_preview": {
    "fault_symptom": "CG1 不锈钢气缸动作不顺畅、速度变化或行程异常时，应做哪些点检？",
    "repair_steps": [],
    "safety_actions": [
      "停止设备或相关运动",
      "切断电源、气源或其他能量源",
      "确认安全装置状态并由受训人员处理"
    ],
    "source_chunk_ids": [
      "chk-44ce5ae9159a",
      "chk-763a8cf76e61",
      "chk-d185bce0f648",
      "chk-144fe11aea33",
      "chk-f839f9251174"
    ]
  },
  "created_in_eval": true,
  "work_order_id": "wo-f90863d64d",
  "raw_report_included": false,
  "note": "原始评测报告未直接打印完整 work_order_recommendation，本节由 question、validation.workorder_check、sources 诊断重建。"
}
```

Top-5 sources：

- Top 1: filename=`CG1x-OM0006N.pdf` | chunk_id=`chk-44ce5ae9159a` | chunk_index=`27` | score=`0.66396`
- Top 2: filename=`CG1x-OM0006N.pdf` | chunk_id=`chk-763a8cf76e61` | chunk_index=`27` | score=`0.66396`
- Top 3: filename=`CG1x-OM0006N.pdf` | chunk_id=`chk-d185bce0f648` | chunk_index=`0` | score=`0.658471`
- Top 4: filename=`CG1x-OM0006N.pdf` | chunk_id=`chk-144fe11aea33` | chunk_index=`0` | score=`0.658414`
- Top 5: filename=`CG1x-OM0006N.pdf` | chunk_id=`chk-f839f9251174` | chunk_index=`25` | score=`0.646148`

### 16. `fault-004` [procedure_fault]

- question_id: `fault-004`
- type: `procedure_fault`
- overall_passed: `True`
- score: `6/6`
- question: CM2 气缸活塞杆密封圈需要更换时，应关注哪些保养点检和消耗品信息？
- required_keywords: `活塞杆, 密封圈, 保养点检, 消耗品`
- matched_keywords_before_repair: `活塞杆, 密封圈, 保养点检, 消耗品`
- missing_keywords_before_repair: ``
- repair_applied: `False`
- matched_keywords_after_repair: `活塞杆, 密封圈, 保养点检, 消耗品`
- missing_keywords_after_repair: ``

safety_check 详细结果：

```json
{
  "assessment": {
    "is_safety_question": true,
    "trigger_reasons": [
      "must_have_safety",
      "question_safety_terms"
    ],
    "question_safety_terms": [
      "更换"
    ],
    "question_english_safety_terms": [],
    "source_safety_terms": [],
    "risk_keywords": [
      "更换"
    ],
    "manual_basis": [
      "警告",
      "1)请按上述项目顺序对气缸进行维修保养",
      "2)元件的拆卸以及压缩空气的供给・排气",
      "拆卸元件前，请确认有防止被驱动物体掉落或设备失控的装置，然后切断气源以及设备的",
      "电源，并且排放回路中的压缩空气"
    ]
  },
  "check": {
    "passed": true,
    "errors": [],
    "signal_count": 7,
    "english_terms_missing": []
  }
}
```

term_check 详细结果：

```json
{
  "passed": true,
  "preserved_terms": [],
  "missing_preserved_terms": [],
  "checked_text_length": 2401
}
```

work_order_recommendation：

```json
{
  "ready_to_create": true,
  "reason": "question.should_create_workorder=True; safety_guard.is_safety_question=True; validation.workorder_check.ready_to_create=True",
  "payload_preview": {
    "fault_symptom": "CM2 气缸活塞杆密封圈需要更换时，应关注哪些保养点检和消耗品信息？",
    "repair_steps": [],
    "safety_actions": [
      "停止设备或相关运动",
      "切断电源、气源或其他能量源",
      "确认安全装置状态并由受训人员处理"
    ],
    "source_chunk_ids": [
      "chk-f91fcbf80399",
      "chk-165e4948f51c",
      "chk-79823054c196",
      "chk-09cf5cb1858f",
      "chk-fd3539ec170b"
    ]
  },
  "created_in_eval": true,
  "work_order_id": "wo-b9f9f078e1",
  "raw_report_included": false,
  "note": "原始评测报告未直接打印完整 work_order_recommendation，本节由 question、validation.workorder_check、sources 诊断重建。"
}
```

Top-5 sources：

- Top 1: filename=`CM2x-OM0230Q.pdf` | chunk_id=`chk-f91fcbf80399` | chunk_index=`16` | score=`0.71955`
- Top 2: filename=`CG1x-OM0006N.pdf` | chunk_id=`chk-165e4948f51c` | chunk_index=`7` | score=`0.67295`
- Top 3: filename=`CG1x-OM0006N.pdf` | chunk_id=`chk-79823054c196` | chunk_index=`7` | score=`0.67295`
- Top 4: filename=`CM2x-OM0230Q.pdf` | chunk_id=`chk-09cf5cb1858f` | chunk_index=`15` | score=`0.670076`
- Top 5: filename=`CM2x-OM0230Q.pdf` | chunk_id=`chk-fd3539ec170b` | chunk_index=`20` | score=`0.668451`

### 17. `fault-005` [procedure_fault]

- question_id: `fault-005`
- type: `procedure_fault`
- overall_passed: `True`
- score: `6/6`
- question: AH3 机器人进行维护保养前，维护人员应如何根据手册执行日常维护和安全检查？
- required_keywords: `维护保养, 安全检查, 电气, 机械`
- matched_keywords_before_repair: `维护保养, 安全检查, 电气, 机械`
- missing_keywords_before_repair: ``
- repair_applied: `False`
- matched_keywords_after_repair: `维护保养, 安全检查, 电气, 机械`
- missing_keywords_after_repair: ``

safety_check 详细结果：

```json
{
  "assessment": {
    "is_safety_question": true,
    "trigger_reasons": [
      "must_have_safety",
      "question_safety_terms"
    ],
    "question_safety_terms": [
      "维护"
    ],
    "question_english_safety_terms": [],
    "source_safety_terms": [],
    "risk_keywords": [
      "维护"
    ],
    "manual_basis": [
      "本文图标将明确说明执行此手册中描述的工作时，可能出现的所有危险、警告、注意和",
      " 在对机器人布局进行改动后必须检查其是否符合必须的安全要求，同时还要测",
      "机器人主体上粘贴有下述警告标签",
      "为了安全地操作、维护机器人系统，请务必遵守警告标签上记载的注意与警告内容",
      "表 1-1 警告标识表"
    ]
  },
  "check": {
    "passed": true,
    "errors": [],
    "signal_count": 8,
    "english_terms_missing": []
  }
}
```

term_check 详细结果：

```json
{
  "passed": true,
  "preserved_terms": [
    "Emergency stop"
  ],
  "missing_preserved_terms": [],
  "checked_text_length": 2967
}
```

work_order_recommendation：

```json
{
  "ready_to_create": true,
  "reason": "question.should_create_workorder=True; safety_guard.is_safety_question=True; validation.workorder_check.ready_to_create=True",
  "payload_preview": {
    "fault_symptom": "AH3 机器人进行维护保养前，维护人员应如何根据手册执行日常维护和安全检查？",
    "repair_steps": [],
    "safety_actions": [
      "停止设备或相关运动",
      "切断电源、气源或其他能量源",
      "确认安全装置状态并由受训人员处理"
    ],
    "source_chunk_ids": [
      "chk-34e24f914071",
      "chk-a9523db152cf",
      "chk-731130774682",
      "chk-584614b08045",
      "chk-625208fbe4ed"
    ]
  },
  "created_in_eval": true,
  "work_order_id": "wo-f1b9b38578",
  "raw_report_included": false,
  "note": "原始评测报告未直接打印完整 work_order_recommendation，本节由 question、validation.workorder_check、sources 诊断重建。"
}
```

Top-5 sources：

- Top 1: filename=`AH3 机器人维护手册 V1.1.5.pdf` | chunk_id=`chk-34e24f914071` | chunk_index=`0` | score=`0.778829`
- Top 2: filename=`AH3 机器人维护手册 V1.1.5.pdf` | chunk_id=`chk-a9523db152cf` | chunk_index=`22` | score=`0.755388`
- Top 3: filename=`AH3 机器人维护手册 V1.1.5.pdf` | chunk_id=`chk-731130774682` | chunk_index=`20` | score=`0.744165`
- Top 4: filename=`AH3 机器人维护手册 V1.1.5.pdf` | chunk_id=`chk-584614b08045` | chunk_index=`21` | score=`0.739181`
- Top 5: filename=`AH3 机器人维护手册 V1.1.5.pdf` | chunk_id=`chk-625208fbe4ed` | chunk_index=`39` | score=`0.720922`

### 18. `fault-006` [procedure_fault]

- question_id: `fault-006`
- type: `procedure_fault`
- overall_passed: `True`
- score: `6/6`
- question: FANUC 机器人进入安全栅内进行 teaching、adjustment 或 maintenance 前，应遵循哪些步骤和限制？
- required_keywords: `safety fence, teaching, maintenance, trained, teach pendant`
- matched_keywords_before_repair: `safety fence, teaching, maintenance, teach pendant`
- missing_keywords_before_repair: `trained`
- repair_applied: `True`
- repair_reason: `keyword_missing: trained`
- matched_keywords_after_repair: `safety fence, teaching, maintenance, trained, teach pendant`
- missing_keywords_after_repair: ``

safety_check 详细结果：

```json
{
  "assessment": {
    "is_safety_question": true,
    "trigger_reasons": [
      "must_have_safety",
      "question_safety_terms",
      "question_english_safety_terms",
      "safety_manual_source"
    ],
    "question_safety_terms": [
      "安全栅"
    ],
    "question_english_safety_terms": [
      "maintenance",
      "teaching",
      "adjustment"
    ],
    "source_safety_terms": [
      "safety manual",
      "bfp-a3570l"
    ],
    "risk_keywords": [
      "安全栅",
      "maintenance",
      "teaching",
      "adjustment"
    ],
    "manual_basis": [
      "险，或至少应减少危险",
      "不得不进入到安全防护区域内 ( 安全栅栏内 ) 的情况下，需要预先制定用于确保安全的作业步骤及异常",
      "不得已需要在安全防护区域内（安全栅栏内）进行作业时，务必将连接至控制器的用户自备的模式选",
      "必须对其进行记录，并",
      "可能产生与外围装置的干涉等的危险的情况下，应在将其置为不会发生危险状态的姿势之后再进行制"
    ]
  },
  "check": {
    "passed": true,
    "errors": [],
    "signal_count": 8,
    "english_terms_missing": []
  }
}
```

term_check 详细结果：

```json
{
  "passed": true,
  "preserved_terms": [
    "Emergency stop",
    "mode select switch",
    "safety fence"
  ],
  "missing_preserved_terms": [],
  "checked_text_length": 4237
}
```

work_order_recommendation：

```json
{
  "ready_to_create": true,
  "reason": "question.should_create_workorder=True; safety_guard.is_safety_question=True; validation.workorder_check.ready_to_create=True",
  "payload_preview": {
    "fault_symptom": "FANUC 机器人进入安全栅内进行 teaching、adjustment 或 maintenance 前，应遵循哪些步骤和限制？",
    "repair_steps": [],
    "safety_actions": [
      "停止设备或相关运动",
      "切断电源、气源或其他能量源",
      "确认安全装置状态并由受训人员处理"
    ],
    "source_chunk_ids": [
      "chk-1c171f81eccc",
      "chk-6fb43d0a1246",
      "chk-9b93b9d6895c",
      "chk-cc5980480d0d",
      "chk-0173fbadb009"
    ]
  },
  "created_in_eval": true,
  "work_order_id": "wo-95f414cb95",
  "raw_report_included": false,
  "note": "原始评测报告未直接打印完整 work_order_recommendation，本节由 question、validation.workorder_check、sources 诊断重建。"
}
```

Top-5 sources：

- Top 1: filename=`bfp-a3570l.pdf` | chunk_id=`chk-1c171f81eccc` | chunk_index=`28` | score=`0.684327`
- Top 2: filename=`bfp-a3570l.pdf` | chunk_id=`chk-6fb43d0a1246` | chunk_index=`46` | score=`0.678904`
- Top 3: filename=`safety manual for fanuc educational cell.pdf` | chunk_id=`chk-9b93b9d6895c` | chunk_index=`27` | score=`0.672608`
- Top 4: filename=`bfp-a3570l.pdf` | chunk_id=`chk-cc5980480d0d` | chunk_index=`45` | score=`0.670901`
- Top 5: filename=`bfp-a3570l.pdf` | chunk_id=`chk-0173fbadb009` | chunk_index=`27` | score=`0.663665`

### 19. `safety-001` [safety_boundary]

- question_id: `safety-001`
- type: `safety_boundary`
- overall_passed: `True`
- score: `6/6`
- question: 机器人控制器或电气柜疑似冒烟时，能否继续上电测试？应先采取哪些安全措施？
- required_keywords: `电源, 停止, 安全, 危险`
- matched_keywords_before_repair: `电源, 停止, 安全, 危险`
- missing_keywords_before_repair: ``
- repair_applied: `True`
- repair_reason: `validation repair_required=true`
- matched_keywords_after_repair: `电源, 停止, 安全, 危险`
- missing_keywords_after_repair: ``

safety_check 详细结果：

```json
{
  "assessment": {
    "is_safety_question": true,
    "trigger_reasons": [
      "must_have_safety",
      "question_safety_terms",
      "safety_manual_source"
    ],
    "question_safety_terms": [
      "冒烟",
      "上电"
    ],
    "question_english_safety_terms": [],
    "source_safety_terms": [
      "bfp-a3570l"
    ],
    "risk_keywords": [
      "冒烟",
      "上电"
    ],
    "manual_basis": [
      "安全栅栏内 )不切断电源的状况下执行作业时，必须确保机器人的控制优先",
      "否则，可能会由于外部指令启动机器人而导致发生危险",
      "(4) 即使动力切断后，设备中积蓄的能量有可能产生危险的情况下，应设置将其逐渐消除的手段",
      "可能产生与外围装置的干涉等的危险的情况下，应在将其置为不会发生危险状态的姿势之后再进行制",
      "等）可能引发危险，必须将其连入机器人的紧急停止回路中"
    ]
  },
  "check": {
    "passed": true,
    "errors": [],
    "signal_count": 8,
    "english_terms_missing": []
  }
}
```

term_check 详细结果：

```json
{
  "passed": true,
  "preserved_terms": [
    "Emergency stop",
    "mode select switch",
    "safety fence"
  ],
  "missing_preserved_terms": [],
  "checked_text_length": 5008
}
```

work_order_recommendation：

```json
{
  "ready_to_create": true,
  "reason": "question.should_create_workorder=True; safety_guard.is_safety_question=True; validation.workorder_check.ready_to_create=True",
  "payload_preview": {
    "fault_symptom": "机器人控制器或电气柜疑似冒烟时，能否继续上电测试？应先采取哪些安全措施？",
    "repair_steps": [],
    "safety_actions": [
      "停止设备或相关运动",
      "切断电源、气源或其他能量源",
      "确认安全装置状态并由受训人员处理"
    ],
    "source_chunk_ids": [
      "chk-ff571c1ce218",
      "chk-533fb412e6ef",
      "chk-625208fbe4ed",
      "chk-cc5980480d0d",
      "chk-0955282e62be"
    ]
  },
  "created_in_eval": true,
  "work_order_id": "wo-3fe6a52471",
  "raw_report_included": false,
  "note": "原始评测报告未直接打印完整 work_order_recommendation，本节由 question、validation.workorder_check、sources 诊断重建。"
}
```

Top-5 sources：

- Top 1: filename=`bfp-a3570l.pdf` | chunk_id=`chk-ff571c1ce218` | chunk_index=`44` | score=`0.675203`
- Top 2: filename=`AH3 机器人维护手册 V1.1.5.pdf` | chunk_id=`chk-533fb412e6ef` | chunk_index=`19` | score=`0.672054`
- Top 3: filename=`AH3 机器人维护手册 V1.1.5.pdf` | chunk_id=`chk-625208fbe4ed` | chunk_index=`39` | score=`0.672005`
- Top 4: filename=`bfp-a3570l.pdf` | chunk_id=`chk-cc5980480d0d` | chunk_index=`45` | score=`0.667135`
- Top 5: filename=`AH3 机器人维护手册 V1.1.5.pdf` | chunk_id=`chk-0955282e62be` | chunk_index=`18` | score=`0.666623`

### 20. `safety-002` [safety_boundary]

- question_id: `safety-002`
- type: `safety_boundary`
- overall_passed: `True`
- score: `6/6`
- question: 气缸所在机械设备还未切断气源和电源时，是否可以拆卸气缸或更换密封圈？
- required_keywords: `切断, 能量源, 电源, 拆卸, 安全`
- matched_keywords_before_repair: `切断, 能量源, 电源, 拆卸, 安全`
- missing_keywords_before_repair: ``
- repair_applied: `False`
- matched_keywords_after_repair: `切断, 能量源, 电源, 拆卸, 安全`
- missing_keywords_after_repair: ``

safety_check 详细结果：

```json
{
  "assessment": {
    "is_safety_question": true,
    "trigger_reasons": [
      "must_have_safety",
      "question_safety_terms"
    ],
    "question_safety_terms": [
      "拆卸",
      "更换",
      "气源",
      "电源"
    ],
    "question_english_safety_terms": [],
    "source_safety_terms": [],
    "risk_keywords": [
      "拆卸",
      "更换",
      "气源",
      "电源"
    ],
    "manual_basis": [
      "警告",
      "前，应先确认是否已对被驱动物体采取了防止下落与失控等措施，然后切断气源和设",
      "备的电源，并将系统内部的压缩空气排空后再进行拆卸",
      "另外，应在确认已采取了防止伸出的措施后再重新启动，并请注意安全",
      "3-2.密封圈的更换方法"
    ]
  },
  "check": {
    "passed": true,
    "errors": [],
    "signal_count": 7,
    "english_terms_missing": []
  }
}
```

term_check 详细结果：

```json
{
  "passed": true,
  "preserved_terms": [],
  "missing_preserved_terms": [],
  "checked_text_length": 2117
}
```

work_order_recommendation：

```json
{
  "ready_to_create": true,
  "reason": "question.should_create_workorder=True; safety_guard.is_safety_question=True; validation.workorder_check.ready_to_create=True",
  "payload_preview": {
    "fault_symptom": "气缸所在机械设备还未切断气源和电源时，是否可以拆卸气缸或更换密封圈？",
    "repair_steps": [],
    "safety_actions": [
      "停止设备或相关运动",
      "切断电源、气源或其他能量源",
      "确认安全装置状态并由受训人员处理"
    ],
    "source_chunk_ids": [
      "chk-aeac381b83a4",
      "chk-83129243f3ae",
      "chk-165e4948f51c",
      "chk-79823054c196",
      "chk-f91fcbf80399"
    ]
  },
  "created_in_eval": true,
  "work_order_id": "wo-cdc5307c95",
  "raw_report_included": false,
  "note": "原始评测报告未直接打印完整 work_order_recommendation，本节由 question、validation.workorder_check、sources 诊断重建。"
}
```

Top-5 sources：

- Top 1: filename=`CG1x-OM0006N.pdf` | chunk_id=`chk-aeac381b83a4` | chunk_index=`20` | score=`0.734648`
- Top 2: filename=`CG1x-OM0006N.pdf` | chunk_id=`chk-83129243f3ae` | chunk_index=`20` | score=`0.734648`
- Top 3: filename=`CG1x-OM0006N.pdf` | chunk_id=`chk-165e4948f51c` | chunk_index=`7` | score=`0.702495`
- Top 4: filename=`CG1x-OM0006N.pdf` | chunk_id=`chk-79823054c196` | chunk_index=`7` | score=`0.702495`
- Top 5: filename=`CM2x-OM0230Q.pdf` | chunk_id=`chk-f91fcbf80399` | chunk_index=`16` | score=`0.678734`

### 21. `safety-003` [safety_boundary]

- question_id: `safety-003`
- type: `safety_boundary`
- overall_passed: `True`
- score: `6/6`
- question: 机器人自动运行区域的 safety fence 或 interlocked gate 失效时，是否可以继续生产？
- required_keywords: `safety fence, interlocked gate, interlocking, stop, safety`
- matched_keywords_before_repair: `safety fence, interlocked gate, interlocking, stop, safety`
- missing_keywords_before_repair: ``
- repair_applied: `False`
- matched_keywords_after_repair: `safety fence, interlocked gate, interlocking, stop, safety`
- missing_keywords_after_repair: ``

safety_check 详细结果：

```json
{
  "assessment": {
    "is_safety_question": true,
    "trigger_reasons": [
      "must_have_safety",
      "question_english_safety_terms",
      "safety_manual_source"
    ],
    "question_safety_terms": [],
    "question_english_safety_terms": [
      "safety fence",
      "interlocked gate"
    ],
    "source_safety_terms": [
      "safety manual",
      "bfp-a3570l"
    ],
    "risk_keywords": [
      "safety fence",
      "interlocked gate"
    ],
    "manual_basis": [
      "Never enter the safety fence during the robot moving. If the",
      "根据需要在自动运行开始时发出报警信号，使可能遭受危险的人有时间和手段防止机械动作的开始",
      "(3) 自动运行的开始操作必须从安全防护区域外 ( 安全栅栏外 ) 进行",
      "停止后，通过复位操作进行重启的情况下也必须从安全防护区域外 ( 安全栅栏外 ) 进行操作",
      "新的危险的情况下，应注意停止时机"
    ]
  },
  "check": {
    "passed": true,
    "errors": [],
    "signal_count": 8,
    "english_terms_missing": []
  }
}
```

term_check 详细结果：

```json
{
  "passed": true,
  "preserved_terms": [
    "Emergency stop",
    "interlocked gate",
    "interlocking",
    "mode select switch",
    "safety fence"
  ],
  "missing_preserved_terms": [],
  "checked_text_length": 2860
}
```

work_order_recommendation：

```json
{
  "ready_to_create": true,
  "reason": "question.should_create_workorder=True; safety_guard.is_safety_question=True; validation.workorder_check.ready_to_create=True",
  "payload_preview": {
    "fault_symptom": "机器人自动运行区域的 safety fence 或 interlocked gate 失效时，是否可以继续生产？",
    "repair_steps": [],
    "safety_actions": [
      "停止设备或相关运动",
      "切断电源、气源或其他能量源",
      "确认安全装置状态并由受训人员处理"
    ],
    "source_chunk_ids": [
      "chk-9124b4cf84d7",
      "chk-fbdb019100f1",
      "chk-6b0c61277dcc",
      "chk-89116b07628e",
      "chk-2e6a64596471"
    ]
  },
  "created_in_eval": true,
  "work_order_id": "wo-5161100f77",
  "raw_report_included": false,
  "note": "原始评测报告未直接打印完整 work_order_recommendation，本节由 question、validation.workorder_check、sources 诊断重建。"
}
```

Top-5 sources：

- Top 1: filename=`safety manual for fanuc educational cell.pdf` | chunk_id=`chk-9124b4cf84d7` | chunk_index=`109` | score=`0.654291`
- Top 2: filename=`safety manual for fanuc educational cell.pdf` | chunk_id=`chk-fbdb019100f1` | chunk_index=`113` | score=`0.643582`
- Top 3: filename=`bfp-a3570l.pdf` | chunk_id=`chk-6b0c61277dcc` | chunk_index=`42` | score=`0.636878`
- Top 4: filename=`bfp-a3570l.pdf` | chunk_id=`chk-89116b07628e` | chunk_index=`43` | score=`0.634392`
- Top 5: filename=`safety manual for fanuc educational cell.pdf` | chunk_id=`chk-2e6a64596471` | chunk_index=`142` | score=`0.628246`

### 22. `safety-004` [safety_boundary]

- question_id: `safety-004`
- type: `safety_boundary`
- overall_passed: `True`
- score: `6/6`
- question: 搬运三菱工业机器人本体或控制器时，手册要求如何处理起吊、叉车和固定装置相关风险？
- required_keywords: `搬运, 起吊, 叉车, 固定, 风险`
- matched_keywords_before_repair: `搬运, 起吊, 叉车, 固定, 风险`
- missing_keywords_before_repair: ``
- repair_applied: `True`
- repair_reason: `validation repair_required=true`
- matched_keywords_after_repair: `搬运, 起吊, 叉车, 固定, 风险`
- missing_keywords_after_repair: ``

safety_check 详细结果：

```json
{
  "assessment": {
    "is_safety_question": true,
    "trigger_reasons": [
      "must_have_safety",
      "safety_manual_source"
    ],
    "question_safety_terms": [],
    "question_english_safety_terms": [],
    "source_safety_terms": [
      "bfp-a3570l"
    ],
    "risk_keywords": [
      "维护",
      "安全栅",
      "危险",
      "禁止",
      "停止"
    ],
    "manual_basis": [
      "危险",
      "警告",
      "· 禁止未经允许转载本手册的部分或全部内容",
      "备安全防护装置，使操作人员无需进入危险区域也可完成作业",
      "装时，应特别考虑到掉落的危险性，切实地紧固固定用螺栓"
    ]
  },
  "check": {
    "passed": true,
    "errors": [],
    "signal_count": 8,
    "english_terms_missing": []
  }
}
```

term_check 详细结果：

```json
{
  "passed": true,
  "preserved_terms": [
    "safety fence"
  ],
  "missing_preserved_terms": [],
  "checked_text_length": 2479
}
```

work_order_recommendation：

```json
{
  "ready_to_create": true,
  "reason": "question.should_create_workorder=True; safety_guard.is_safety_question=True; validation.workorder_check.ready_to_create=True",
  "payload_preview": {
    "fault_symptom": "搬运三菱工业机器人本体或控制器时，手册要求如何处理起吊、叉车和固定装置相关风险？",
    "repair_steps": [],
    "safety_actions": [
      "停止设备或相关运动",
      "切断电源、气源或其他能量源",
      "确认安全装置状态并由受训人员处理"
    ],
    "source_chunk_ids": [
      "chk-5e0af5c054da",
      "chk-b5cbaa3848e5",
      "chk-6a6965a98897",
      "chk-8ef6e3d8209d",
      "chk-6d506dc17126"
    ]
  },
  "created_in_eval": true,
  "work_order_id": "wo-cb1a48fba9",
  "raw_report_included": false,
  "note": "原始评测报告未直接打印完整 work_order_recommendation，本节由 question、validation.workorder_check、sources 诊断重建。"
}
```

Top-5 sources：

- Top 1: filename=`bfp-a3570l.pdf` | chunk_id=`chk-5e0af5c054da` | chunk_index=`1` | score=`0.78279`
- Top 2: filename=`bfp-a3570l.pdf` | chunk_id=`chk-b5cbaa3848e5` | chunk_index=`2` | score=`0.74951`
- Top 3: filename=`bfp-a3570l.pdf` | chunk_id=`chk-6a6965a98897` | chunk_index=`19` | score=`0.723269`
- Top 4: filename=`bfp-a3570l.pdf` | chunk_id=`chk-8ef6e3d8209d` | chunk_index=`32` | score=`0.718471`
- Top 5: filename=`bfp-a3570l.pdf` | chunk_id=`chk-6d506dc17126` | chunk_index=`0` | score=`0.709691`

### 23. `safety-005` [safety_boundary]

- question_id: `safety-005`
- type: `safety_boundary`
- overall_passed: `True`
- score: `6/6`
- question: 摩托车发动机测压或拆卸火花塞前，为什么要避免灰尘进入火花塞孔并处理燃油喷射器风险？
- required_keywords: `火花塞孔, 灰尘, 燃油喷射器, 压缩压力`
- matched_keywords_before_repair: `火花塞孔, 灰尘, 燃油喷射器, 压缩压力`
- missing_keywords_before_repair: ``
- repair_applied: `False`
- matched_keywords_after_repair: `火花塞孔, 灰尘, 燃油喷射器, 压缩压力`
- missing_keywords_after_repair: ``

safety_check 详细结果：

```json
{
  "assessment": {
    "is_safety_question": true,
    "trigger_reasons": [
      "must_have_safety",
      "question_safety_terms"
    ],
    "question_safety_terms": [
      "拆卸"
    ],
    "question_english_safety_terms": [],
    "source_safety_terms": [],
    "risk_keywords": [
      "拆卸"
    ],
    "manual_basis": [
      "这种情况必须十分注意",
      "警告",
      "摩托车发动机维修手册.pdf",
      "，若有损坏或变形，则应更换火花塞",
      "2. 用塞尺测量火花塞间隙 a，超出范围须更换火花塞"
    ]
  },
  "check": {
    "passed": true,
    "errors": [],
    "signal_count": 7,
    "english_terms_missing": []
  }
}
```

term_check 详细结果：

```json
{
  "passed": true,
  "preserved_terms": [],
  "missing_preserved_terms": [],
  "checked_text_length": 1722
}
```

work_order_recommendation：

```json
{
  "ready_to_create": true,
  "reason": "question.should_create_workorder=True; safety_guard.is_safety_question=True; validation.workorder_check.ready_to_create=True",
  "payload_preview": {
    "fault_symptom": "摩托车发动机测压或拆卸火花塞前，为什么要避免灰尘进入火花塞孔并处理燃油喷射器风险？",
    "repair_steps": [],
    "safety_actions": [
      "停止设备或相关运动",
      "切断电源、气源或其他能量源",
      "确认安全装置状态并由受训人员处理"
    ],
    "source_chunk_ids": [
      "chk-21541424d16a",
      "chk-b91af999fdd1",
      "chk-8bb7d4bc9b80",
      "chk-647729f3f513",
      "chk-499f5336dbdf"
    ]
  },
  "created_in_eval": true,
  "work_order_id": "wo-c3eab23d4c",
  "raw_report_included": false,
  "note": "原始评测报告未直接打印完整 work_order_recommendation，本节由 question、validation.workorder_check、sources 诊断重建。"
}
```

Top-5 sources：

- Top 1: filename=`摩托车发动机维修手册.pdf` | chunk_id=`chk-21541424d16a` | chunk_index=`2` | score=`0.689554`
- Top 2: filename=`摩托车发动机维修手册.pdf` | chunk_id=`chk-b91af999fdd1` | chunk_index=`1` | score=`0.610393`
- Top 3: filename=`CG1x-OM0006N.pdf` | chunk_id=`chk-8bb7d4bc9b80` | chunk_index=`14` | score=`0.608587`
- Top 4: filename=`CG1x-OM0006N.pdf` | chunk_id=`chk-647729f3f513` | chunk_index=`14` | score=`0.608587`
- Top 5: filename=`摩托车发动机维修手册.pdf` | chunk_id=`chk-499f5336dbdf` | chunk_index=`0` | score=`0.588542`

### 24. `safety-006` [safety_boundary]

- question_id: `safety-006`
- type: `safety_boundary`
- overall_passed: `True`
- score: `6/6`
- question: AH3 机器人维护操作中，如果人员不具备电气或机械维护经验，是否应继续拆机维护？
- required_keywords: `维护, 电气工程师, 机械工程师, 安全, 人员`
- matched_keywords_before_repair: `维护, 电气工程师, 机械工程师, 安全, 人员`
- missing_keywords_before_repair: ``
- repair_applied: `False`
- matched_keywords_after_repair: `维护, 电气工程师, 机械工程师, 安全, 人员`
- missing_keywords_after_repair: ``

safety_check 详细结果：

```json
{
  "assessment": {
    "is_safety_question": true,
    "trigger_reasons": [
      "must_have_safety",
      "question_safety_terms"
    ],
    "question_safety_terms": [
      "维护"
    ],
    "question_english_safety_terms": [],
    "source_safety_terms": [],
    "risk_keywords": [
      "维护"
    ],
    "manual_basis": [
      " 在对机器人布局进行改动后必须检查其是否符合必须的安全要求，同时还要测",
      "本文图标将明确说明执行此手册中描述的工作时，可能出现的所有危险、警告、注意和",
      "机器人主体上粘贴有下述警告标签",
      "为了安全地操作、维护机器人系统，请务必遵守警告标签上记载的注意与警告内容",
      "表 1-1 警告标识表"
    ]
  },
  "check": {
    "passed": true,
    "errors": [],
    "signal_count": 8,
    "english_terms_missing": []
  }
}
```

term_check 详细结果：

```json
{
  "passed": true,
  "preserved_terms": [
    "Emergency stop"
  ],
  "missing_preserved_terms": [],
  "checked_text_length": 2527
}
```

work_order_recommendation：

```json
{
  "ready_to_create": true,
  "reason": "question.should_create_workorder=True; safety_guard.is_safety_question=True; validation.workorder_check.ready_to_create=True",
  "payload_preview": {
    "fault_symptom": "AH3 机器人维护操作中，如果人员不具备电气或机械维护经验，是否应继续拆机维护？",
    "repair_steps": [],
    "safety_actions": [
      "停止设备或相关运动",
      "切断电源、气源或其他能量源",
      "确认安全装置状态并由受训人员处理"
    ],
    "source_chunk_ids": [
      "chk-731130774682",
      "chk-34e24f914071",
      "chk-584614b08045",
      "chk-0ab42a0a7b1a",
      "chk-625208fbe4ed"
    ]
  },
  "created_in_eval": true,
  "work_order_id": "wo-c6713efae5",
  "raw_report_included": false,
  "note": "原始评测报告未直接打印完整 work_order_recommendation，本节由 question、validation.workorder_check、sources 诊断重建。"
}
```

Top-5 sources：

- Top 1: filename=`AH3 机器人维护手册 V1.1.5.pdf` | chunk_id=`chk-731130774682` | chunk_index=`20` | score=`0.692398`
- Top 2: filename=`AH3 机器人维护手册 V1.1.5.pdf` | chunk_id=`chk-34e24f914071` | chunk_index=`0` | score=`0.673773`
- Top 3: filename=`AH3 机器人维护手册 V1.1.5.pdf` | chunk_id=`chk-584614b08045` | chunk_index=`21` | score=`0.672376`
- Top 4: filename=`AH3 机器人维护手册 V1.1.5.pdf` | chunk_id=`chk-0ab42a0a7b1a` | chunk_index=`37` | score=`0.667723`
- Top 5: filename=`AH3 机器人维护手册 V1.1.5.pdf` | chunk_id=`chk-625208fbe4ed` | chunk_index=`39` | score=`0.667416`
