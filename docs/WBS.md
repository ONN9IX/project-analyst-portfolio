# WBS — структура работ и артефактов

## A. Технические этапы исходного продукта (фактический контекст README)

| Код | Этап | Контрольный источник | Интерпретация |
|---|---|---|---|
| A1 | Основа приложения, авторизация, доступы | [Stage 1 manual #33](https://github.com/ONN9IX/smart-garden/issues/33) | Техническая поставка |
| A2 | Группы, дети, родители | [Stage 2 #52](https://github.com/ONN9IX/smart-garden/issues/52) | Техническая поставка |
| A3 | Сотрудники и посещаемость | [Stage 3 #86](https://github.com/ONN9IX/smart-garden/issues/86) | Техническая приёмка |
| A4 | Audit и объявления | [Stage 4 #98](https://github.com/ONN9IX/smart-garden/issues/98) | Техническая приёмка |
| A5 | Security/operations/CI | [Stage 5 #117](https://github.com/ONN9IX/smart-garden/issues/117) | Техническая приёмка |
| A6 | Кабинеты и взаимодействия ролей | [Stage 6 #152](https://github.com/ONN9IX/smart-garden/issues/152) | Техническая приёмка |

**Важно:** даты закрытия соответствующих Issue — контрольные точки в GitHub, не доказательство фактической длительности всего этапа. Статус приёмки подтверждён техническим README, но не является допуском к production на реальных ПДн.

## B. Направления развития (backlog, без согласованных дат)

- B1 — [#187](https://github.com/ONN9IX/smart-garden/issues/187): подготовка синтетического пилота / go-no-go.
- B2 — [#223](https://github.com/ONN9IX/smart-garden/issues/223): privacy/152-ФЗ.
- B3 — [#162](https://github.com/ONN9IX/smart-garden/issues/162): универсальные профили.
- B4 — [#189](https://github.com/ONN9IX/smart-garden/issues/189): PWA.
- B5 — [#197](https://github.com/ONN9IX/smart-garden/issues/197): оповещения о посещаемости.
- B6 — [#204](https://github.com/ONN9IX/smart-garden/issues/204): инфраструктурная автоматизация.

Открытая Issue означает существование запроса/задачи, а не одобренный план реализации.

## C. WBS отдельного аналитического кейса (выполнено)

- C1.0 Сбор: GitHub API → CSV Issues и PR.
- C2.0 Качество: типы, уникальность, статус/даты, ссылки на источники.
- C3.0 Метрики: доля закрытых Issues, статус PR, ежедневная динамика.
- C4.0 SQL: схема, загрузка, бизнес-запросы.
- C5.0 Excel: исходные таблицы, KPI и диаграммы.
- C6.0 Управленческие материалы: charter, WBS, roadmap, риски, RACI, status report.
- C7.0 Проверки: Python `unittest`, повторный расчёт.
