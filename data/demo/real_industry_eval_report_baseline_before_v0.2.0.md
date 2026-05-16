# Real Industry RAG Eval Report

- generated_at: `2026-05-11 16:56:34`
- api_base_url: `http://127.0.0.1:8000/api`
- question_count: `24`
- passed_count: `14`
- failed_count: `10`
- total_score: `110`
- max_score: `120`
- top_k: `5`

> 用途：针对真实工业资料集合评测 RAG 检索、结构化回答、安全提醒和 WorkOrder 保存完整性。自动评分用于筛查问题，最终相关性仍建议人工复核。

## 01. smoke-001 [smoke]

- 问题：摩托车发动机火花塞应该如何检查和安装？请给出关键间隙和拧紧要求。
- expected_documents: `摩托车发动机维修手册.pdf`
- expected_keywords: `火花塞, 0.7, 0.9, 20, N·m`
- must_have_safety: `False`
- should_create_workorder: `False`
- 自动评分：`5/5`
- overall_passed: `True`

### 命中文档

- Top-3 命中：`True`
- 命中文档：`摩托车发动机维修手册.pdf`
- Top-3 文档：`摩托车发动机维修手册.pdf, 摩托车发动机维修手册.pdf, 摩托车发动机维修手册.pdf`

### Sources

- Top 1: filename=`摩托车发动机维修手册.pdf` | chunk_id=`chk-21541424d16a` | chunk_index=`2` | score=`0.798056`
- Top 2: filename=`摩托车发动机维修手册.pdf` | chunk_id=`chk-b91af999fdd1` | chunk_index=`1` | score=`0.714229`
- Top 3: filename=`摩托车发动机维修手册.pdf` | chunk_id=`chk-4d7f935536ae` | chunk_index=`13` | score=`0.697461`
- Top 4: filename=`摩托车发动机维修手册.pdf` | chunk_id=`chk-dfb84876691d` | chunk_index=`5` | score=`0.692629`
- Top 5: filename=`摩托车发动机维修手册.pdf` | chunk_id=`chk-ab08fbdb930b` | chunk_index=`9` | score=`0.688442`

### 关键内容检查

- 通过：`True`
- 缺失关键词：``

### 安全提醒检查

- 通过：`True`
- safety_notes 数量：`5`

### WorkOrder 检查

- 通过：`True`
- 已创建：`False`
- detail_loaded：`False`
- work_order_id：``

### 人工备注栏

- Top-3 来源是否正确：
- 回答是否忠实于资料：
- 关键参数/步骤是否可用：
- 安全提醒是否充分：
- 备注：

## 02. smoke-002 [smoke]

- 问题：AH3 机器人维护手册主要面向哪些维护内容？日常维护时应关注哪些安全提示？
- expected_documents: `AH3 机器人维护手册 V1.1.5.pdf`
- expected_keywords: `AH3, 维护, 安全, 检查`
- must_have_safety: `True`
- should_create_workorder: `False`
- 自动评分：`5/5`
- overall_passed: `True`

### 命中文档

- Top-3 命中：`True`
- 命中文档：`AH3 机器人维护手册 V1.1.5.pdf`
- Top-3 文档：`AH3 机器人维护手册 V1.1.5.pdf, AH3 机器人维护手册 V1.1.5.pdf, AH3 机器人维护手册 V1.1.5.pdf`

### Sources

- Top 1: filename=`AH3 机器人维护手册 V1.1.5.pdf` | chunk_id=`chk-34e24f914071` | chunk_index=`0` | score=`0.816121`
- Top 2: filename=`AH3 机器人维护手册 V1.1.5.pdf` | chunk_id=`chk-584614b08045` | chunk_index=`21` | score=`0.746096`
- Top 3: filename=`AH3 机器人维护手册 V1.1.5.pdf` | chunk_id=`chk-f836f9d469f8` | chunk_index=`15` | score=`0.73096`
- Top 4: filename=`AH3 机器人维护手册 V1.1.5.pdf` | chunk_id=`chk-7d795b762e99` | chunk_index=`4` | score=`0.72899`
- Top 5: filename=`AH3 机器人维护手册 V1.1.5.pdf` | chunk_id=`chk-a9523db152cf` | chunk_index=`22` | score=`0.726166`

### 关键内容检查

- 通过：`True`
- 缺失关键词：``

### 安全提醒检查

- 通过：`True`
- safety_notes 数量：`7`

### WorkOrder 检查

- 通过：`True`
- 已创建：`False`
- detail_loaded：`False`
- work_order_id：``

### 人工备注栏

- Top-3 来源是否正确：
- 回答是否忠实于资料：
- 关键参数/步骤是否可用：
- 安全提醒是否充分：
- 备注：

## 03. smoke-003 [smoke]

- 问题：bfp-a3570l 安全手册中的剩余风险地图和剩余风险一览表是用来做什么的？
- expected_documents: `bfp-a3570l.pdf`
- expected_keywords: `剩余风险, 保护措施, 危险, 警告`
- must_have_safety: `True`
- should_create_workorder: `False`
- 自动评分：`5/5`
- overall_passed: `True`

### 命中文档

- Top-3 命中：`True`
- 命中文档：`bfp-a3570l.pdf`
- Top-3 文档：`bfp-a3570l.pdf, bfp-a3570l.pdf, bfp-a3570l.pdf`

### Sources

- Top 1: filename=`bfp-a3570l.pdf` | chunk_id=`chk-6d506dc17126` | chunk_index=`0` | score=`0.692703`
- Top 2: filename=`bfp-a3570l.pdf` | chunk_id=`chk-5e0af5c054da` | chunk_index=`1` | score=`0.58272`
- Top 3: filename=`bfp-a3570l.pdf` | chunk_id=`chk-27c9c85ace60` | chunk_index=`18` | score=`0.571339`
- Top 4: filename=`safety manual for fanuc educational cell.pdf` | chunk_id=`chk-2fa410c18c12` | chunk_index=`7` | score=`0.567688`
- Top 5: filename=`AH3 机器人维护手册 V1.1.5.pdf` | chunk_id=`chk-f836f9d469f8` | chunk_index=`15` | score=`0.550905`

### 关键内容检查

- 通过：`True`
- 缺失关键词：``

### 安全提醒检查

- 通过：`True`
- safety_notes 数量：`3`

### WorkOrder 检查

- 通过：`True`
- 已创建：`False`
- detail_loaded：`False`
- work_order_id：``

### 人工备注栏

- Top-3 来源是否正确：
- 回答是否忠实于资料：
- 关键参数/步骤是否可用：
- 安全提醒是否充分：
- 备注：

## 04. smoke-004 [smoke]

- 问题：FANUC educational cell 安全手册说明了哪些机器人安全使用注意事项？
- expected_documents: `safety manual for fanuc educational cell.pdf`
- expected_keywords: `FANUC, safety, robot, emergency`
- must_have_safety: `True`
- should_create_workorder: `False`
- 自动评分：`4/5`
- overall_passed: `False`

### 命中文档

- Top-3 命中：`True`
- 命中文档：`safety manual for fanuc educational cell.pdf`
- Top-3 文档：`safety manual for fanuc educational cell.pdf, bfp-a3570l.pdf, safety manual for fanuc educational cell.pdf`

### Sources

- Top 1: filename=`safety manual for fanuc educational cell.pdf` | chunk_id=`chk-c16663488d97` | chunk_index=`5` | score=`0.699092`
- Top 2: filename=`bfp-a3570l.pdf` | chunk_id=`chk-5e0af5c054da` | chunk_index=`1` | score=`0.683044`
- Top 3: filename=`safety manual for fanuc educational cell.pdf` | chunk_id=`chk-9b93b9d6895c` | chunk_index=`27` | score=`0.672677`
- Top 4: filename=`safety manual for fanuc educational cell.pdf` | chunk_id=`chk-877bfd5c9b10` | chunk_index=`150` | score=`0.671748`
- Top 5: filename=`bfp-a3570l.pdf` | chunk_id=`chk-6a6965a98897` | chunk_index=`19` | score=`0.665423`

### 关键内容检查

- 通过：`False`
- 缺失关键词：`robot, emergency`

### 安全提醒检查

- 通过：`True`
- safety_notes 数量：`8`

### WorkOrder 检查

- 通过：`True`
- 已创建：`False`
- detail_loaded：`False`
- work_order_id：``

### 自动检查问题

- answer/structured fields missing expected keywords: ['robot', 'emergency']

### 人工备注栏

- Top-3 来源是否正确：
- 回答是否忠实于资料：
- 关键参数/步骤是否可用：
- 安全提醒是否充分：
- 备注：

## 05. smoke-005 [smoke]

- 问题：CM2x-OM0230Q 气缸手册包含哪些主要章节？
- expected_documents: `CM2x-OM0230Q.pdf`
- expected_keywords: `气缸, 产品规格, 设置方法, 保养点检`
- must_have_safety: `False`
- should_create_workorder: `False`
- 自动评分：`5/5`
- overall_passed: `True`

### 命中文档

- Top-3 命中：`True`
- 命中文档：`CM2x-OM0230Q.pdf`
- Top-3 文档：`CM2x-OM0230Q.pdf, CG1x-OM0006N.pdf, CG1x-OM0006N.pdf`

### Sources

- Top 1: filename=`CM2x-OM0230Q.pdf` | chunk_id=`chk-65d6cca0f77c` | chunk_index=`0` | score=`0.676752`
- Top 2: filename=`CG1x-OM0006N.pdf` | chunk_id=`chk-144fe11aea33` | chunk_index=`0` | score=`0.616203`
- Top 3: filename=`CG1x-OM0006N.pdf` | chunk_id=`chk-d185bce0f648` | chunk_index=`0` | score=`0.61618`
- Top 4: filename=`CG1x-OM0006N.pdf` | chunk_id=`chk-44ce5ae9159a` | chunk_index=`27` | score=`0.556921`
- Top 5: filename=`CG1x-OM0006N.pdf` | chunk_id=`chk-763a8cf76e61` | chunk_index=`27` | score=`0.556921`

### 关键内容检查

- 通过：`True`
- 缺失关键词：``

### 安全提醒检查

- 通过：`True`
- safety_notes 数量：`2`

### WorkOrder 检查

- 通过：`True`
- 已创建：`False`
- detail_loaded：`False`
- work_order_id：``

### 人工备注栏

- Top-3 来源是否正确：
- 回答是否忠实于资料：
- 关键参数/步骤是否可用：
- 安全提醒是否充分：
- 备注：

## 06. smoke-006 [smoke]

- 问题：CG1x-OM0006N 不锈钢气缸手册包含哪些维修保养和故障对策内容？
- expected_documents: `CG1x-OM0006N.pdf`
- expected_keywords: `不锈钢气缸, 维修保养, 点检, 故障`
- must_have_safety: `False`
- should_create_workorder: `False`
- 自动评分：`5/5`
- overall_passed: `True`

### 命中文档

- Top-3 命中：`True`
- 命中文档：`CG1x-OM0006N.pdf`
- Top-3 文档：`CG1x-OM0006N.pdf, CG1x-OM0006N.pdf, CM2x-OM0230Q.pdf`

### Sources

- Top 1: filename=`CG1x-OM0006N.pdf` | chunk_id=`chk-144fe11aea33` | chunk_index=`0` | score=`0.730002`
- Top 2: filename=`CG1x-OM0006N.pdf` | chunk_id=`chk-d185bce0f648` | chunk_index=`0` | score=`0.729974`
- Top 3: filename=`CM2x-OM0230Q.pdf` | chunk_id=`chk-65d6cca0f77c` | chunk_index=`0` | score=`0.664283`
- Top 4: filename=`CG1x-OM0006N.pdf` | chunk_id=`chk-44ce5ae9159a` | chunk_index=`27` | score=`0.611462`
- Top 5: filename=`CG1x-OM0006N.pdf` | chunk_id=`chk-763a8cf76e61` | chunk_index=`27` | score=`0.611462`

### 关键内容检查

- 通过：`True`
- 缺失关键词：``

### 安全提醒检查

- 通过：`True`
- safety_notes 数量：`2`

### WorkOrder 检查

- 通过：`True`
- 已创建：`False`
- detail_loaded：`False`
- work_order_id：``

### 人工备注栏

- Top-3 来源是否正确：
- 回答是否忠实于资料：
- 关键参数/步骤是否可用：
- 安全提醒是否充分：
- 备注：

## 07. param-001 [parameter]

- 问题：摩托车发动机火花塞间隙标准值是多少？安装火花塞的拧紧力矩是多少？
- expected_documents: `摩托车发动机维修手册.pdf`
- expected_keywords: `0.7, 0.9, 20, N·m`
- must_have_safety: `False`
- should_create_workorder: `False`
- 自动评分：`5/5`
- overall_passed: `True`

### 命中文档

- Top-3 命中：`True`
- 命中文档：`摩托车发动机维修手册.pdf`
- Top-3 文档：`摩托车发动机维修手册.pdf, 摩托车发动机维修手册.pdf, 摩托车发动机维修手册.pdf`

### Sources

- Top 1: filename=`摩托车发动机维修手册.pdf` | chunk_id=`chk-21541424d16a` | chunk_index=`2` | score=`0.747561`
- Top 2: filename=`摩托车发动机维修手册.pdf` | chunk_id=`chk-d026f9ac3955` | chunk_index=`6` | score=`0.653299`
- Top 3: filename=`摩托车发动机维修手册.pdf` | chunk_id=`chk-dfb84876691d` | chunk_index=`5` | score=`0.634031`
- Top 4: filename=`摩托车发动机维修手册.pdf` | chunk_id=`chk-4d7f935536ae` | chunk_index=`13` | score=`0.632085`
- Top 5: filename=`摩托车发动机维修手册.pdf` | chunk_id=`chk-ab08fbdb930b` | chunk_index=`9` | score=`0.631945`

### 关键内容检查

- 通过：`True`
- 缺失关键词：``

### 安全提醒检查

- 通过：`True`
- safety_notes 数量：`7`

### WorkOrder 检查

- 通过：`True`
- 已创建：`False`
- detail_loaded：`False`
- work_order_id：``

### 人工备注栏

- Top-3 来源是否正确：
- 回答是否忠实于资料：
- 关键参数/步骤是否可用：
- 安全提醒是否充分：
- 备注：

## 08. param-002 [parameter]

- 问题：摩托车发动机测量压缩压力时，标准压缩压力范围是多少？
- expected_documents: `摩托车发动机维修手册.pdf`
- expected_keywords: `1300, 1900, 500, 900, kPa`
- must_have_safety: `True`
- should_create_workorder: `False`
- 自动评分：`5/5`
- overall_passed: `True`

### 命中文档

- Top-3 命中：`True`
- 命中文档：`摩托车发动机维修手册.pdf`
- Top-3 文档：`摩托车发动机维修手册.pdf, 摩托车发动机维修手册.pdf, 摩托车发动机维修手册.pdf`

### Sources

- Top 1: filename=`摩托车发动机维修手册.pdf` | chunk_id=`chk-21541424d16a` | chunk_index=`2` | score=`0.687767`
- Top 2: filename=`摩托车发动机维修手册.pdf` | chunk_id=`chk-d026f9ac3955` | chunk_index=`6` | score=`0.621322`
- Top 3: filename=`摩托车发动机维修手册.pdf` | chunk_id=`chk-dfb84876691d` | chunk_index=`5` | score=`0.610289`
- Top 4: filename=`CG1x-OM0006N.pdf` | chunk_id=`chk-4896a18d171f` | chunk_index=`8` | score=`0.602476`
- Top 5: filename=`CG1x-OM0006N.pdf` | chunk_id=`chk-724a5de67b0b` | chunk_index=`8` | score=`0.602476`

### 关键内容检查

- 通过：`True`
- 缺失关键词：``

### 安全提醒检查

- 通过：`True`
- safety_notes 数量：`8`

### WorkOrder 检查

- 通过：`True`
- 已创建：`False`
- detail_loaded：`False`
- work_order_id：``

### 人工备注栏

- Top-3 来源是否正确：
- 回答是否忠实于资料：
- 关键参数/步骤是否可用：
- 安全提醒是否充分：
- 备注：

## 09. param-003 [parameter]

- 问题：CM2 系列气缸使用前需要确认哪些空气源和速度控制相关条件？
- expected_documents: `CM2x-OM0230Q.pdf`
- expected_keywords: `使用空气, 速度控制, 气缸, 调整`
- must_have_safety: `False`
- should_create_workorder: `False`
- 自动评分：`4/5`
- overall_passed: `False`

### 命中文档

- Top-3 命中：`True`
- 命中文档：`CM2x-OM0230Q.pdf`
- Top-3 文档：`CM2x-OM0230Q.pdf, CG1x-OM0006N.pdf, CG1x-OM0006N.pdf`

### Sources

- Top 1: filename=`CM2x-OM0230Q.pdf` | chunk_id=`chk-65d6cca0f77c` | chunk_index=`0` | score=`0.669675`
- Top 2: filename=`CG1x-OM0006N.pdf` | chunk_id=`chk-8bb7d4bc9b80` | chunk_index=`14` | score=`0.623545`
- Top 3: filename=`CG1x-OM0006N.pdf` | chunk_id=`chk-647729f3f513` | chunk_index=`14` | score=`0.623545`
- Top 4: filename=`CG1x-OM0006N.pdf` | chunk_id=`chk-730b481cb2cb` | chunk_index=`15` | score=`0.619911`
- Top 5: filename=`CG1x-OM0006N.pdf` | chunk_id=`chk-bcaa8d1cf42c` | chunk_index=`15` | score=`0.619911`

### 关键内容检查

- 通过：`False`
- 缺失关键词：`调整`

### 安全提醒检查

- 通过：`True`
- safety_notes 数量：`0`

### WorkOrder 检查

- 通过：`True`
- 已创建：`False`
- detail_loaded：`False`
- work_order_id：``

### 自动检查问题

- answer/structured fields missing expected keywords: ['调整']

### 人工备注栏

- Top-3 来源是否正确：
- 回答是否忠实于资料：
- 关键参数/步骤是否可用：
- 安全提醒是否充分：
- 备注：

## 10. param-004 [parameter]

- 问题：CG1 系列不锈钢气缸磁性开关安装时，安装螺钉的紧固力矩要求是什么？
- expected_documents: `CG1x-OM0006N.pdf`
- expected_keywords: `磁性开关, M4, 1, 1.2, N`
- must_have_safety: `False`
- should_create_workorder: `False`
- 自动评分：`5/5`
- overall_passed: `True`

### 命中文档

- Top-3 命中：`True`
- 命中文档：`CG1x-OM0006N.pdf`
- Top-3 文档：`CG1x-OM0006N.pdf, CG1x-OM0006N.pdf, CM2x-OM0230Q.pdf`

### Sources

- Top 1: filename=`CG1x-OM0006N.pdf` | chunk_id=`chk-c1f980dc39dd` | chunk_index=`19` | score=`0.701569`
- Top 2: filename=`CG1x-OM0006N.pdf` | chunk_id=`chk-e3133442503d` | chunk_index=`19` | score=`0.701569`
- Top 3: filename=`CM2x-OM0230Q.pdf` | chunk_id=`chk-a22f19291795` | chunk_index=`11` | score=`0.677936`
- Top 4: filename=`CG1x-OM0006N.pdf` | chunk_id=`chk-65a4ebe4d849` | chunk_index=`18` | score=`0.670755`
- Top 5: filename=`CG1x-OM0006N.pdf` | chunk_id=`chk-2fdc017d9509` | chunk_index=`18` | score=`0.670755`

### 关键内容检查

- 通过：`True`
- 缺失关键词：``

### 安全提醒检查

- 通过：`True`
- safety_notes 数量：`2`

### WorkOrder 检查

- 通过：`True`
- 已创建：`False`
- detail_loaded：`False`
- work_order_id：``

### 人工备注栏

- Top-3 来源是否正确：
- 回答是否忠实于资料：
- 关键参数/步骤是否可用：
- 安全提醒是否充分：
- 备注：

## 11. param-005 [parameter]

- 问题：FANUC 机器人控制器相关安全功能中，Emergency stop、mode select switch、deadman switch 分别属于哪些安全控制主题？
- expected_documents: `safety manual for fanuc educational cell.pdf`
- expected_keywords: `Emergency stop, mode select, deadman, teach pendant`
- must_have_safety: `True`
- should_create_workorder: `False`
- 自动评分：`4/5`
- overall_passed: `False`

### 命中文档

- Top-3 命中：`True`
- 命中文档：`safety manual for fanuc educational cell.pdf`
- Top-3 文档：`safety manual for fanuc educational cell.pdf, safety manual for fanuc educational cell.pdf, safety manual for fanuc educational cell.pdf`

### Sources

- Top 1: filename=`safety manual for fanuc educational cell.pdf` | chunk_id=`chk-97c9bf4b7bb0` | chunk_index=`105` | score=`0.629936`
- Top 2: filename=`safety manual for fanuc educational cell.pdf` | chunk_id=`chk-11932d0c1547` | chunk_index=`74` | score=`0.608202`
- Top 3: filename=`safety manual for fanuc educational cell.pdf` | chunk_id=`chk-a5646801d304` | chunk_index=`93` | score=`0.589858`
- Top 4: filename=`bfp-a3570l.pdf` | chunk_id=`chk-03d68abdce49` | chunk_index=`37` | score=`0.589603`
- Top 5: filename=`safety manual for fanuc educational cell.pdf` | chunk_id=`chk-433ca6a8c08f` | chunk_index=`61` | score=`0.588695`

### 关键内容检查

- 通过：`False`
- 缺失关键词：`teach pendant`

### 安全提醒检查

- 通过：`True`
- safety_notes 数量：`4`

### WorkOrder 检查

- 通过：`True`
- 已创建：`False`
- detail_loaded：`False`
- work_order_id：``

### 自动检查问题

- answer/structured fields missing expected keywords: ['teach pendant']

### 人工备注栏

- Top-3 来源是否正确：
- 回答是否忠实于资料：
- 关键参数/步骤是否可用：
- 安全提醒是否充分：
- 备注：

## 12. param-006 [parameter]

- 问题：AH3 机器人维护资料中版本号、发布日期和适用对象信息是什么？
- expected_documents: `AH3 机器人维护手册 V1.1.5.pdf`
- expected_keywords: `V1.1.5, 2023-05-15, 维护保养工程师, 机械工程师`
- must_have_safety: `False`
- should_create_workorder: `False`
- 自动评分：`5/5`
- overall_passed: `True`

### 命中文档

- Top-3 命中：`True`
- 命中文档：`AH3 机器人维护手册 V1.1.5.pdf`
- Top-3 文档：`AH3 机器人维护手册 V1.1.5.pdf, AH3 机器人维护手册 V1.1.5.pdf, AH3 机器人维护手册 V1.1.5.pdf`

### Sources

- Top 1: filename=`AH3 机器人维护手册 V1.1.5.pdf` | chunk_id=`chk-34e24f914071` | chunk_index=`0` | score=`0.772888`
- Top 2: filename=`AH3 机器人维护手册 V1.1.5.pdf` | chunk_id=`chk-7d795b762e99` | chunk_index=`4` | score=`0.7009`
- Top 3: filename=`AH3 机器人维护手册 V1.1.5.pdf` | chunk_id=`chk-f836f9d469f8` | chunk_index=`15` | score=`0.686481`
- Top 4: filename=`AH3 机器人维护手册 V1.1.5.pdf` | chunk_id=`chk-8b0e4a3e46b4` | chunk_index=`2` | score=`0.678943`
- Top 5: filename=`AH3 机器人维护手册 V1.1.5.pdf` | chunk_id=`chk-c382291794e7` | chunk_index=`9` | score=`0.667205`

### 关键内容检查

- 通过：`True`
- 缺失关键词：``

### 安全提醒检查

- 通过：`True`
- safety_notes 数量：`1`

### WorkOrder 检查

- 通过：`True`
- 已创建：`False`
- detail_loaded：`False`
- work_order_id：``

### 人工备注栏

- Top-3 来源是否正确：
- 回答是否忠实于资料：
- 关键参数/步骤是否可用：
- 安全提醒是否充分：
- 备注：

## 13. fault-001 [procedure_fault]

- 问题：摩托车发动机压缩压力低于标准下限时，应该如何判断是活塞环、气缸还是气门相关问题？
- expected_documents: `摩托车发动机维修手册.pdf`
- expected_keywords: `压缩压力, 机油, 活塞, 气门, 气缸`
- must_have_safety: `True`
- should_create_workorder: `True`
- 自动评分：`5/5`
- overall_passed: `True`

### 命中文档

- Top-3 命中：`True`
- 命中文档：`摩托车发动机维修手册.pdf`
- Top-3 文档：`摩托车发动机维修手册.pdf, CG1x-OM0006N.pdf, CG1x-OM0006N.pdf`

### Sources

- Top 1: filename=`摩托车发动机维修手册.pdf` | chunk_id=`chk-21541424d16a` | chunk_index=`2` | score=`0.667088`
- Top 2: filename=`CG1x-OM0006N.pdf` | chunk_id=`chk-3319bc93ff5a` | chunk_index=`24` | score=`0.639796`
- Top 3: filename=`CG1x-OM0006N.pdf` | chunk_id=`chk-238df46741e0` | chunk_index=`24` | score=`0.639796`
- Top 4: filename=`CM2x-OM0230Q.pdf` | chunk_id=`chk-9bbda50b82bf` | chunk_index=`18` | score=`0.636661`
- Top 5: filename=`CG1x-OM0006N.pdf` | chunk_id=`chk-f839f9251174` | chunk_index=`25` | score=`0.626194`

### 关键内容检查

- 通过：`True`
- 缺失关键词：``

### 安全提醒检查

- 通过：`True`
- safety_notes 数量：`8`

### WorkOrder 检查

- 通过：`True`
- 已创建：`True`
- detail_loaded：`True`
- work_order_id：`wo-f4ff5a7d42`

### 人工备注栏

- Top-3 来源是否正确：
- 回答是否忠实于资料：
- 关键参数/步骤是否可用：
- 安全提醒是否充分：
- 备注：

## 14. fault-002 [procedure_fault]

- 问题：摩托车起动电机无法正常带动发动机转动时，应按哪些部件和步骤排查？
- expected_documents: `摩托车发动机维修手册.pdf`
- expected_keywords: `起动电机, 拆卸, 安装, 检查`
- must_have_safety: `True`
- should_create_workorder: `True`
- 自动评分：`5/5`
- overall_passed: `True`

### 命中文档

- Top-3 命中：`True`
- 命中文档：`摩托车发动机维修手册.pdf`
- Top-3 文档：`摩托车发动机维修手册.pdf, 摩托车发动机维修手册.pdf, 摩托车发动机维修手册.pdf`

### Sources

- Top 1: filename=`摩托车发动机维修手册.pdf` | chunk_id=`chk-f33f51c42f12` | chunk_index=`3` | score=`0.738417`
- Top 2: filename=`摩托车发动机维修手册.pdf` | chunk_id=`chk-b91af999fdd1` | chunk_index=`1` | score=`0.672429`
- Top 3: filename=`摩托车发动机维修手册.pdf` | chunk_id=`chk-d5195cfdd53e` | chunk_index=`23` | score=`0.669248`
- Top 4: filename=`摩托车发动机维修手册.pdf` | chunk_id=`chk-dfb84876691d` | chunk_index=`5` | score=`0.665144`
- Top 5: filename=`摩托车发动机维修手册.pdf` | chunk_id=`chk-30c0b27e17aa` | chunk_index=`24` | score=`0.660712`

### 关键内容检查

- 通过：`True`
- 缺失关键词：``

### 安全提醒检查

- 通过：`True`
- safety_notes 数量：`8`

### WorkOrder 检查

- 通过：`True`
- 已创建：`True`
- detail_loaded：`True`
- work_order_id：`wo-5eedc9e938`

### 人工备注栏

- Top-3 来源是否正确：
- 回答是否忠实于资料：
- 关键参数/步骤是否可用：
- 安全提醒是否充分：
- 备注：

## 15. fault-003 [procedure_fault]

- 问题：CG1 不锈钢气缸动作不顺畅、速度变化或行程异常时，应做哪些点检？
- expected_documents: `CG1x-OM0006N.pdf`
- expected_keywords: `点检, 作动, 速度, 行程, 安装螺钉`
- must_have_safety: `True`
- should_create_workorder: `True`
- 自动评分：`4/5`
- overall_passed: `False`

### 命中文档

- Top-3 命中：`True`
- 命中文档：`CG1x-OM0006N.pdf`
- Top-3 文档：`CG1x-OM0006N.pdf, CG1x-OM0006N.pdf, CG1x-OM0006N.pdf`

### Sources

- Top 1: filename=`CG1x-OM0006N.pdf` | chunk_id=`chk-44ce5ae9159a` | chunk_index=`27` | score=`0.66396`
- Top 2: filename=`CG1x-OM0006N.pdf` | chunk_id=`chk-763a8cf76e61` | chunk_index=`27` | score=`0.66396`
- Top 3: filename=`CG1x-OM0006N.pdf` | chunk_id=`chk-d185bce0f648` | chunk_index=`0` | score=`0.658471`
- Top 4: filename=`CG1x-OM0006N.pdf` | chunk_id=`chk-144fe11aea33` | chunk_index=`0` | score=`0.658414`
- Top 5: filename=`CG1x-OM0006N.pdf` | chunk_id=`chk-f839f9251174` | chunk_index=`25` | score=`0.646148`

### 关键内容检查

- 通过：`False`
- 缺失关键词：`安装螺钉`

### 安全提醒检查

- 通过：`True`
- safety_notes 数量：`3`

### WorkOrder 检查

- 通过：`True`
- 已创建：`True`
- detail_loaded：`True`
- work_order_id：`wo-bc42e95279`

### 自动检查问题

- answer/structured fields missing expected keywords: ['安装螺钉']

### 人工备注栏

- Top-3 来源是否正确：
- 回答是否忠实于资料：
- 关键参数/步骤是否可用：
- 安全提醒是否充分：
- 备注：

## 16. fault-004 [procedure_fault]

- 问题：CM2 气缸活塞杆密封圈需要更换时，应关注哪些保养点检和消耗品信息？
- expected_documents: `CM2x-OM0230Q.pdf`
- expected_keywords: `活塞杆, 密封圈, 保养点检, 消耗品`
- must_have_safety: `True`
- should_create_workorder: `True`
- 自动评分：`4/5`
- overall_passed: `False`

### 命中文档

- Top-3 命中：`True`
- 命中文档：`CM2x-OM0230Q.pdf`
- Top-3 文档：`CM2x-OM0230Q.pdf, CG1x-OM0006N.pdf, CG1x-OM0006N.pdf`

### Sources

- Top 1: filename=`CM2x-OM0230Q.pdf` | chunk_id=`chk-f91fcbf80399` | chunk_index=`16` | score=`0.71955`
- Top 2: filename=`CG1x-OM0006N.pdf` | chunk_id=`chk-165e4948f51c` | chunk_index=`7` | score=`0.67295`
- Top 3: filename=`CG1x-OM0006N.pdf` | chunk_id=`chk-79823054c196` | chunk_index=`7` | score=`0.67295`
- Top 4: filename=`CM2x-OM0230Q.pdf` | chunk_id=`chk-09cf5cb1858f` | chunk_index=`15` | score=`0.670076`
- Top 5: filename=`CM2x-OM0230Q.pdf` | chunk_id=`chk-fd3539ec170b` | chunk_index=`20` | score=`0.668451`

### 关键内容检查

- 通过：`False`
- 缺失关键词：`保养点检`

### 安全提醒检查

- 通过：`True`
- safety_notes 数量：`9`

### WorkOrder 检查

- 通过：`True`
- 已创建：`True`
- detail_loaded：`True`
- work_order_id：`wo-14fa9978ee`

### 自动检查问题

- answer/structured fields missing expected keywords: ['保养点检']

### 人工备注栏

- Top-3 来源是否正确：
- 回答是否忠实于资料：
- 关键参数/步骤是否可用：
- 安全提醒是否充分：
- 备注：

## 17. fault-005 [procedure_fault]

- 问题：AH3 机器人进行维护保养前，维护人员应如何根据手册执行日常维护和安全检查？
- expected_documents: `AH3 机器人维护手册 V1.1.5.pdf`
- expected_keywords: `维护保养, 安全检查, 电气, 机械`
- must_have_safety: `True`
- should_create_workorder: `True`
- 自动评分：`4/5`
- overall_passed: `False`

### 命中文档

- Top-3 命中：`True`
- 命中文档：`AH3 机器人维护手册 V1.1.5.pdf`
- Top-3 文档：`AH3 机器人维护手册 V1.1.5.pdf, AH3 机器人维护手册 V1.1.5.pdf, AH3 机器人维护手册 V1.1.5.pdf`

### Sources

- Top 1: filename=`AH3 机器人维护手册 V1.1.5.pdf` | chunk_id=`chk-34e24f914071` | chunk_index=`0` | score=`0.778829`
- Top 2: filename=`AH3 机器人维护手册 V1.1.5.pdf` | chunk_id=`chk-a9523db152cf` | chunk_index=`22` | score=`0.755388`
- Top 3: filename=`AH3 机器人维护手册 V1.1.5.pdf` | chunk_id=`chk-731130774682` | chunk_index=`20` | score=`0.744165`
- Top 4: filename=`AH3 机器人维护手册 V1.1.5.pdf` | chunk_id=`chk-584614b08045` | chunk_index=`21` | score=`0.739181`
- Top 5: filename=`AH3 机器人维护手册 V1.1.5.pdf` | chunk_id=`chk-625208fbe4ed` | chunk_index=`39` | score=`0.720922`

### 关键内容检查

- 通过：`False`
- 缺失关键词：`电气`

### 安全提醒检查

- 通过：`True`
- safety_notes 数量：`13`

### WorkOrder 检查

- 通过：`True`
- 已创建：`True`
- detail_loaded：`True`
- work_order_id：`wo-1f12a9f069`

### 自动检查问题

- answer/structured fields missing expected keywords: ['电气']

### 人工备注栏

- Top-3 来源是否正确：
- 回答是否忠实于资料：
- 关键参数/步骤是否可用：
- 安全提醒是否充分：
- 备注：

## 18. fault-006 [procedure_fault]

- 问题：FANUC 机器人进入安全栅内进行 teaching、adjustment 或 maintenance 前，应遵循哪些步骤和限制？
- expected_documents: `safety manual for fanuc educational cell.pdf`
- expected_keywords: `safety fence, teaching, maintenance, trained, teach pendant`
- must_have_safety: `True`
- should_create_workorder: `True`
- 自动评分：`4/5`
- overall_passed: `False`

### 命中文档

- Top-3 命中：`True`
- 命中文档：`safety manual for fanuc educational cell.pdf`
- Top-3 文档：`bfp-a3570l.pdf, bfp-a3570l.pdf, safety manual for fanuc educational cell.pdf`

### Sources

- Top 1: filename=`bfp-a3570l.pdf` | chunk_id=`chk-1c171f81eccc` | chunk_index=`28` | score=`0.684327`
- Top 2: filename=`bfp-a3570l.pdf` | chunk_id=`chk-6fb43d0a1246` | chunk_index=`46` | score=`0.678904`
- Top 3: filename=`safety manual for fanuc educational cell.pdf` | chunk_id=`chk-9b93b9d6895c` | chunk_index=`27` | score=`0.672608`
- Top 4: filename=`bfp-a3570l.pdf` | chunk_id=`chk-cc5980480d0d` | chunk_index=`45` | score=`0.670901`
- Top 5: filename=`bfp-a3570l.pdf` | chunk_id=`chk-0173fbadb009` | chunk_index=`27` | score=`0.663665`

### 关键内容检查

- 通过：`False`
- 缺失关键词：`safety fence, trained, teach pendant`

### 安全提醒检查

- 通过：`True`
- safety_notes 数量：`13`

### WorkOrder 检查

- 通过：`True`
- 已创建：`True`
- detail_loaded：`True`
- work_order_id：`wo-70297557ed`

### 自动检查问题

- answer/structured fields missing expected keywords: ['safety fence', 'trained', 'teach pendant']

### 人工备注栏

- Top-3 来源是否正确：
- 回答是否忠实于资料：
- 关键参数/步骤是否可用：
- 安全提醒是否充分：
- 备注：

## 19. safety-001 [safety_boundary]

- 问题：机器人控制器或电气柜疑似冒烟时，能否继续上电测试？应先采取哪些安全措施？
- expected_documents: `bfp-a3570l.pdf, safety manual for fanuc educational cell.pdf`
- expected_keywords: `电源, 停止, 安全, 危险`
- must_have_safety: `True`
- should_create_workorder: `True`
- 自动评分：`4/5`
- overall_passed: `False`

### 命中文档

- Top-3 命中：`True`
- 命中文档：`bfp-a3570l.pdf`
- Top-3 文档：`bfp-a3570l.pdf, AH3 机器人维护手册 V1.1.5.pdf, AH3 机器人维护手册 V1.1.5.pdf`

### Sources

- Top 1: filename=`bfp-a3570l.pdf` | chunk_id=`chk-ff571c1ce218` | chunk_index=`44` | score=`0.675203`
- Top 2: filename=`AH3 机器人维护手册 V1.1.5.pdf` | chunk_id=`chk-533fb412e6ef` | chunk_index=`19` | score=`0.672054`
- Top 3: filename=`AH3 机器人维护手册 V1.1.5.pdf` | chunk_id=`chk-625208fbe4ed` | chunk_index=`39` | score=`0.672005`
- Top 4: filename=`bfp-a3570l.pdf` | chunk_id=`chk-cc5980480d0d` | chunk_index=`45` | score=`0.667135`
- Top 5: filename=`AH3 机器人维护手册 V1.1.5.pdf` | chunk_id=`chk-0955282e62be` | chunk_index=`18` | score=`0.666623`

### 关键内容检查

- 通过：`False`
- 缺失关键词：`危险`

### 安全提醒检查

- 通过：`True`
- safety_notes 数量：`10`

### WorkOrder 检查

- 通过：`True`
- 已创建：`True`
- detail_loaded：`True`
- work_order_id：`wo-1b26c32b6e`

### 自动检查问题

- answer/structured fields missing expected keywords: ['危险']

### 人工备注栏

- Top-3 来源是否正确：
- 回答是否忠实于资料：
- 关键参数/步骤是否可用：
- 安全提醒是否充分：
- 备注：

## 20. safety-002 [safety_boundary]

- 问题：气缸所在机械设备还未切断气源和电源时，是否可以拆卸气缸或更换密封圈？
- expected_documents: `CG1x-OM0006N.pdf, CM2x-OM0230Q.pdf`
- expected_keywords: `切断, 能量源, 电源, 拆卸, 安全`
- must_have_safety: `True`
- should_create_workorder: `True`
- 自动评分：`4/5`
- overall_passed: `False`

### 命中文档

- Top-3 命中：`True`
- 命中文档：`CG1x-OM0006N.pdf`
- Top-3 文档：`CG1x-OM0006N.pdf, CG1x-OM0006N.pdf, CG1x-OM0006N.pdf`

### Sources

- Top 1: filename=`CG1x-OM0006N.pdf` | chunk_id=`chk-aeac381b83a4` | chunk_index=`20` | score=`0.734619`
- Top 2: filename=`CG1x-OM0006N.pdf` | chunk_id=`chk-83129243f3ae` | chunk_index=`20` | score=`0.734619`
- Top 3: filename=`CG1x-OM0006N.pdf` | chunk_id=`chk-165e4948f51c` | chunk_index=`7` | score=`0.70251`
- Top 4: filename=`CG1x-OM0006N.pdf` | chunk_id=`chk-79823054c196` | chunk_index=`7` | score=`0.70251`
- Top 5: filename=`CM2x-OM0230Q.pdf` | chunk_id=`chk-f91fcbf80399` | chunk_index=`16` | score=`0.678735`

### 关键内容检查

- 通过：`False`
- 缺失关键词：`能量源`

### 安全提醒检查

- 通过：`True`
- safety_notes 数量：`9`

### WorkOrder 检查

- 通过：`True`
- 已创建：`True`
- detail_loaded：`True`
- work_order_id：`wo-efa0bcfc5a`

### 自动检查问题

- answer/structured fields missing expected keywords: ['能量源']

### 人工备注栏

- Top-3 来源是否正确：
- 回答是否忠实于资料：
- 关键参数/步骤是否可用：
- 安全提醒是否充分：
- 备注：

## 21. safety-003 [safety_boundary]

- 问题：机器人自动运行区域的 safety fence 或 interlocked gate 失效时，是否可以继续生产？
- expected_documents: `safety manual for fanuc educational cell.pdf`
- expected_keywords: `safety fence, interlocked gate, interlocking, stop, safety`
- must_have_safety: `True`
- should_create_workorder: `True`
- 自动评分：`4/5`
- overall_passed: `False`

### 命中文档

- Top-3 命中：`True`
- 命中文档：`safety manual for fanuc educational cell.pdf`
- Top-3 文档：`safety manual for fanuc educational cell.pdf, safety manual for fanuc educational cell.pdf, bfp-a3570l.pdf`

### Sources

- Top 1: filename=`safety manual for fanuc educational cell.pdf` | chunk_id=`chk-9124b4cf84d7` | chunk_index=`109` | score=`0.654291`
- Top 2: filename=`safety manual for fanuc educational cell.pdf` | chunk_id=`chk-fbdb019100f1` | chunk_index=`113` | score=`0.643582`
- Top 3: filename=`bfp-a3570l.pdf` | chunk_id=`chk-6b0c61277dcc` | chunk_index=`42` | score=`0.636878`
- Top 4: filename=`bfp-a3570l.pdf` | chunk_id=`chk-89116b07628e` | chunk_index=`43` | score=`0.634392`
- Top 5: filename=`safety manual for fanuc educational cell.pdf` | chunk_id=`chk-2e6a64596471` | chunk_index=`142` | score=`0.628246`

### 关键内容检查

- 通过：`False`
- 缺失关键词：`safety fence, interlocked gate, interlocking, stop`

### 安全提醒检查

- 通过：`True`
- safety_notes 数量：`6`

### WorkOrder 检查

- 通过：`True`
- 已创建：`True`
- detail_loaded：`True`
- work_order_id：`wo-9daf026787`

### 自动检查问题

- answer/structured fields missing expected keywords: ['safety fence', 'interlocked gate', 'interlocking', 'stop']

### 人工备注栏

- Top-3 来源是否正确：
- 回答是否忠实于资料：
- 关键参数/步骤是否可用：
- 安全提醒是否充分：
- 备注：

## 22. safety-004 [safety_boundary]

- 问题：搬运三菱工业机器人本体或控制器时，手册要求如何处理起吊、叉车和固定装置相关风险？
- expected_documents: `bfp-a3570l.pdf`
- expected_keywords: `搬运, 起吊, 叉车, 固定, 风险`
- must_have_safety: `True`
- should_create_workorder: `True`
- 自动评分：`5/5`
- overall_passed: `True`

### 命中文档

- Top-3 命中：`True`
- 命中文档：`bfp-a3570l.pdf`
- Top-3 文档：`bfp-a3570l.pdf, bfp-a3570l.pdf, bfp-a3570l.pdf`

### Sources

- Top 1: filename=`bfp-a3570l.pdf` | chunk_id=`chk-5e0af5c054da` | chunk_index=`1` | score=`0.78279`
- Top 2: filename=`bfp-a3570l.pdf` | chunk_id=`chk-b5cbaa3848e5` | chunk_index=`2` | score=`0.74951`
- Top 3: filename=`bfp-a3570l.pdf` | chunk_id=`chk-6a6965a98897` | chunk_index=`19` | score=`0.723269`
- Top 4: filename=`bfp-a3570l.pdf` | chunk_id=`chk-8ef6e3d8209d` | chunk_index=`32` | score=`0.718471`
- Top 5: filename=`bfp-a3570l.pdf` | chunk_id=`chk-6d506dc17126` | chunk_index=`0` | score=`0.709691`

### 关键内容检查

- 通过：`True`
- 缺失关键词：``

### 安全提醒检查

- 通过：`True`
- safety_notes 数量：`5`

### WorkOrder 检查

- 通过：`True`
- 已创建：`True`
- detail_loaded：`True`
- work_order_id：`wo-3b9ab699d9`

### 人工备注栏

- Top-3 来源是否正确：
- 回答是否忠实于资料：
- 关键参数/步骤是否可用：
- 安全提醒是否充分：
- 备注：

## 23. safety-005 [safety_boundary]

- 问题：摩托车发动机测压或拆卸火花塞前，为什么要避免灰尘进入火花塞孔并处理燃油喷射器风险？
- expected_documents: `摩托车发动机维修手册.pdf`
- expected_keywords: `火花塞孔, 灰尘, 燃油喷射器, 压缩压力`
- must_have_safety: `True`
- should_create_workorder: `True`
- 自动评分：`5/5`
- overall_passed: `True`

### 命中文档

- Top-3 命中：`True`
- 命中文档：`摩托车发动机维修手册.pdf`
- Top-3 文档：`摩托车发动机维修手册.pdf, 摩托车发动机维修手册.pdf, CG1x-OM0006N.pdf`

### Sources

- Top 1: filename=`摩托车发动机维修手册.pdf` | chunk_id=`chk-21541424d16a` | chunk_index=`2` | score=`0.689496`
- Top 2: filename=`摩托车发动机维修手册.pdf` | chunk_id=`chk-b91af999fdd1` | chunk_index=`1` | score=`0.610374`
- Top 3: filename=`CG1x-OM0006N.pdf` | chunk_id=`chk-8bb7d4bc9b80` | chunk_index=`14` | score=`0.608622`
- Top 4: filename=`CG1x-OM0006N.pdf` | chunk_id=`chk-647729f3f513` | chunk_index=`14` | score=`0.608622`
- Top 5: filename=`摩托车发动机维修手册.pdf` | chunk_id=`chk-499f5336dbdf` | chunk_index=`0` | score=`0.58853`

### 关键内容检查

- 通过：`True`
- 缺失关键词：``

### 安全提醒检查

- 通过：`True`
- safety_notes 数量：`3`

### WorkOrder 检查

- 通过：`True`
- 已创建：`True`
- detail_loaded：`True`
- work_order_id：`wo-190cafa736`

### 人工备注栏

- Top-3 来源是否正确：
- 回答是否忠实于资料：
- 关键参数/步骤是否可用：
- 安全提醒是否充分：
- 备注：

## 24. safety-006 [safety_boundary]

- 问题：AH3 机器人维护操作中，如果人员不具备电气或机械维护经验，是否应继续拆机维护？
- expected_documents: `AH3 机器人维护手册 V1.1.5.pdf`
- expected_keywords: `维护, 电气工程师, 机械工程师, 安全, 人员`
- must_have_safety: `True`
- should_create_workorder: `True`
- 自动评分：`5/5`
- overall_passed: `True`

### 命中文档

- Top-3 命中：`True`
- 命中文档：`AH3 机器人维护手册 V1.1.5.pdf`
- Top-3 文档：`AH3 机器人维护手册 V1.1.5.pdf, AH3 机器人维护手册 V1.1.5.pdf, AH3 机器人维护手册 V1.1.5.pdf`

### Sources

- Top 1: filename=`AH3 机器人维护手册 V1.1.5.pdf` | chunk_id=`chk-731130774682` | chunk_index=`20` | score=`0.692398`
- Top 2: filename=`AH3 机器人维护手册 V1.1.5.pdf` | chunk_id=`chk-34e24f914071` | chunk_index=`0` | score=`0.673773`
- Top 3: filename=`AH3 机器人维护手册 V1.1.5.pdf` | chunk_id=`chk-584614b08045` | chunk_index=`21` | score=`0.672376`
- Top 4: filename=`AH3 机器人维护手册 V1.1.5.pdf` | chunk_id=`chk-0ab42a0a7b1a` | chunk_index=`37` | score=`0.667723`
- Top 5: filename=`AH3 机器人维护手册 V1.1.5.pdf` | chunk_id=`chk-625208fbe4ed` | chunk_index=`39` | score=`0.667416`

### 关键内容检查

- 通过：`True`
- 缺失关键词：``

### 安全提醒检查

- 通过：`True`
- safety_notes 数量：`8`

### WorkOrder 检查

- 通过：`True`
- 已创建：`True`
- detail_loaded：`True`
- work_order_id：`wo-9bf28301b5`

### 人工备注栏

- Top-3 来源是否正确：
- 回答是否忠实于资料：
- 关键参数/步骤是否可用：
- 安全提醒是否充分：
- 备注：
