# Real Industry RAG Eval Report v0.2.0

- baseline_report: `data/demo/real_industry_eval_report_baseline_before_v0.2.0.md`
- v0.2.0_raw_report: `data/demo/real_industry_eval_report.md`
- question_count: `24`
- passed_count: `24`
- failed_count: `0`
- total_score: `144`
- max_score: `144`

## 与上一版状态对比

| # | id | type | v0.1.x | v0.2.0 | 状态变化 | v0.2.0 score |
|---:|---|---|---|---|---|---|
| 1 | `smoke-001` | `smoke` | PASS | PASS | 原来通过现在仍通过 | `6/6` |
| 2 | `smoke-002` | `smoke` | PASS | PASS | 原来通过现在仍通过 | `6/6` |
| 3 | `smoke-003` | `smoke` | PASS | PASS | 原来通过现在仍通过 | `6/6` |
| 4 | `smoke-004` | `smoke` | FAIL | PASS | 原来失败现在通过 | `6/6` |
| 5 | `smoke-005` | `smoke` | PASS | PASS | 原来通过现在仍通过 | `6/6` |
| 6 | `smoke-006` | `smoke` | PASS | PASS | 原来通过现在仍通过 | `6/6` |
| 7 | `param-001` | `parameter` | PASS | PASS | 原来通过现在仍通过 | `6/6` |
| 8 | `param-002` | `parameter` | PASS | PASS | 原来通过现在仍通过 | `6/6` |
| 9 | `param-003` | `parameter` | FAIL | PASS | 原来失败现在通过 | `6/6` |
| 10 | `param-004` | `parameter` | PASS | PASS | 原来通过现在仍通过 | `6/6` |
| 11 | `param-005` | `parameter` | FAIL | PASS | 原来失败现在通过 | `6/6` |
| 12 | `param-006` | `parameter` | PASS | PASS | 原来通过现在仍通过 | `6/6` |
| 13 | `fault-001` | `procedure_fault` | PASS | PASS | 原来通过现在仍通过 | `6/6` |
| 14 | `fault-002` | `procedure_fault` | PASS | PASS | 原来通过现在仍通过 | `6/6` |
| 15 | `fault-003` | `procedure_fault` | FAIL | PASS | 原来失败现在通过 | `6/6` |
| 16 | `fault-004` | `procedure_fault` | FAIL | PASS | 原来失败现在通过 | `6/6` |
| 17 | `fault-005` | `procedure_fault` | FAIL | PASS | 原来失败现在通过 | `6/6` |
| 18 | `fault-006` | `procedure_fault` | FAIL | PASS | 原来失败现在通过 | `6/6` |
| 19 | `safety-001` | `safety_boundary` | FAIL | PASS | 原来失败现在通过 | `6/6` |
| 20 | `safety-002` | `safety_boundary` | FAIL | PASS | 原来失败现在通过 | `6/6` |
| 21 | `safety-003` | `safety_boundary` | FAIL | PASS | 原来失败现在通过 | `6/6` |
| 22 | `safety-004` | `safety_boundary` | PASS | PASS | 原来通过现在仍通过 | `6/6` |
| 23 | `safety-005` | `safety_boundary` | PASS | PASS | 原来通过现在仍通过 | `6/6` |
| 24 | `safety-006` | `safety_boundary` | PASS | PASS | 原来通过现在仍通过 | `6/6` |

## 分类统计

- 原来失败现在通过: `10`
- 原来通过现在仍通过: `14`
- 原来失败仍失败: `0`
- 原来通过现在失败: `0`

## 失败题诊断

v0.2.0 本轮 24 题全部通过，无失败题。