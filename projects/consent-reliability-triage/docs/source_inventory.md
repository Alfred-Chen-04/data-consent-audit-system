# Source inventory（工作包 01）

检索时间：2026-09-13 UTC。原始资料保存于 `evidence/sources/`，每份文件都有 SHA-256 和上游 commit。

| 来源 | 本地证据 | 粒度 | 主要字段/用途 | 生成方式与时间 | 许可证/限制 |
|---|---|---|---|---|---|
| AutoConsent coverage | `coverage_c2e9fcd6c22a.json` | rule × region | `sites`, `errors`, `selfTestFailures`, 五类网站列表 | tracker-radar-collector 对 US/DE/GB top 10k 列表爬取；最新来源 commit 2026-08-13 | 仓库 LICENSE 为 MPL-2.0；data 目录未见单独许可证；聚合统计，不是完整逐站日志 |
| coverage 历史 | `coverage_c6983b4e58b6.json`, `coverage_3fa7435a9d40.json` 及 `coverage_history.txt` | snapshot × rule × region | 用于检查 key 和数值变化 | Git 提交记录；最近三份为 2026-08-13、2026-07-31、2026-06-12 | commit 时间不是采集时间；规则、站点列表和爬取条件可能变化 |
| 官方数据说明 | `data__Readme.md` | 字段定义 | 解释 coverage 口径 | 仓库文档 | `unsuccessfulSites` 出现在实际 JSON，但当前说明没有解释 |
| AutoConsent 规则/测试 | `rules__autoconsent__bandcamp.json`, `tests__bandcamp.spec.ts` | rule / test site | detect、opt-out、self-test、样本映射 | 规则文件和 Playwright 测试 | 规则会随版本变化；测试成功不等同于历史 coverage 失败已被解释 |
| 运行入口 | `playwright__runner.ts`, `playwright__content.ts`, `playwright.config.ts` | website × environment × run | 运行、截图和消息日志 | 仓库自带 Playwright harness | 需要依赖、浏览器和可访问网站；本次没有配置地区代理 |
| 公开维护记录 | Git commits、coverage PR #1480 | commit/PR | 解释快照刷新和规则变化 | GitHub | issue/PR 的日期不能替代运行采集日期；不能把维护活动当作故障真值 |

来源完整清单和哈希见 `evidence/sources/manifest.json`。
