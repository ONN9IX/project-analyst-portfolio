# Публикация отдельного Project Analyst Portfolio

Важное условие: **никогда не загружать эти файлы в ONN9IX/smart-garden**. Аналитика размещается исключительно в новом репозитории `ONN9IX/project-analyst-portfolio`.

## Опубликованный репозиторий

Портфолио опубликовано: https://github.com/ONN9IX/project-analyst-portfolio.

## Справочная инструкция для первоначальной публикации на Windows

1. Открой https://github.com/new?name=project-analyst-portfolio.
2. Owner: **ONN9IX**; repository name: **project-analyst-portfolio**; visibility: **Public**.
3. **Не ставь** флажки «Add a README», «Add .gitignore», «Choose a license»: репозиторий должен быть пустым.
4. Нажми **Create repository**.
5. Распакуй `project-analyst-portfolio.zip` на компьютер.
6. Открой папку `project-analyst-portfolio` и дважды щёлкни по **`publish.cmd`**. Для работы нужен установленный [Git for Windows](https://git-scm.com/downloads/win). При необходимости Git запросит вход в GitHub через браузер.
7. Дождись сообщения `Готово: https://github.com/ONN9IX/project-analyst-portfolio`.
8. Открой https://github.com/ONN9IX/project-analyst-portfolio и проверь, что видны README, оба графика, папки `sql/`, `docs/`, `resume/` и Excel-файлы.

Если командный файл завершился ошибкой, **не загружай данные в Smart Garden**. Скопируй текст ошибки и пришли в ChatGPT. Альтернатива: открыть PowerShell в распакованной папке и выполнить `powershell -NoProfile -ExecutionPolicy Bypass -File .\publish.ps1`.

## Перед отправкой резюме работодателям

- В публичных резюме оставлен GitHub. При необходимости добавь контакты в отдельную версию для откликов.
- Ссылка на опубликованное портфолио уже вставлена в резюме.
- Проверь официальное название факультета и описание лично выполненных задач.
- Используй PDF для откликов, DOCX для редактирования.

Скрипты `publish.cmd` и `publish.ps1` работают только из распакованной папки нового аналитического репозитория и **не выполняют операций с Smart Garden**.
