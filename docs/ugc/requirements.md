## Задача
Создать систему отслеживания пользовательских событий на сайте фильмов. Это могут быть клики, просмотры страниц, лайки.
В будущем также может возникнуть потребность отслеживать и другие активности в онлайн-кинотеатре.
Например, может быть полезно узнать, сколько вендоры добавляют новых фильмов каждый месяц.

## Бизнес-требования
### Отслеживание кликов.
Сервис должен собирать данные о кликах пользователя по различным элементам интерфейса, таким как фильмы, трейлеры, категории и другие ключевые элементы сайта.
### Отслеживание просмотров страниц.
Система должна отслеживать, какие страницы (например, страницы фильмов, категорий, акционных предложений) пользователи просматривают и сколько времени проводят на них.
### Отслеживание кастомных событий.
Сервис должен иметь возможность отслеживания следующих кастомных событий:
* **Смена качества видео.** Запись каждого изменения качества просматриваемого видео (например, переключение с 720p на 1080p).
* **Просмотр видео до конца.** Фиксация каждого просмотра фильма или шоу до конца. Это может помочь анализировать, насколько контент удерживает внимание пользователя.
* **Использование фильтров поиска.** Запись использования различных фильтров при поиске фильмов (например, по жанру, рейтингу, актерам).

## Функциональные требования
* Система должна обрабатывать события пользователей на сайте.
* Система должна иметь возможность сохранять пользовательские события.

## Нефункциональные требования
* **Масштабируемость**: система должна быть способна обслуживать до 10,000 одновременных пользователей в пиковые периоды, такие как выходные, праздничные дни или акции.
* **Производительность**: время отклика системы на любую пользовательскую команду не должно превышать одну секунду 95% времени. Верхний предел для максимального времени ответа не должен превышать две секунды. Система должна визуально откликаться на действие пользователя в течение 200 миллисекунд.
* **Надёжность**: система должна обеспечивать бесперебойное функционирование с минимальным временем простоя. Оно должно иметь uptime не менее 99.99% в год. Все пользовательские данные должны регулярно резервироваться, и система должна быть способна восстанавливаться после сбоев без потери данных.

## Use Cases

### Общий
#### Сценарий использования
* Обработка события пользователей сайта
#### Акторы
* Пользователь (User), сайт (UI, FrontEnd), система обработки событий (System)
#### Предусловия
* На сайте реализован функционал отслеживания пользовательских событий (клики, просмотры страниц, лайки, и т.д.)
#### Цель
* Система успешно сохраняет пользовательское событие
#### Описание
1. Пользователь совершает действие на сайте (ставит "лайк", переходит на другую страницу сайта по внутренней ссылке, запускает видео, и т.д.), генерирует событие.
2. Сайт отслеживает пользовательское событие и передает метаданные (id event, id film, datetime event, и т.д.) события в систему.
3. Система обрабатывает событие пользователя по переданным метаданным.
4. Система сохраняет пользовательское событие.

### Пользователь ставит "лайк" (как пример)
#### Сценарий использования
* Пользователь ставит "лайк" на понравившейся фильм.
#### Акторы
* Пользователь, сайт, система.
#### Предусловия
* На сайте есть функционал отслеживания действий пользователя при проставлении "лайка".
#### Цель
* Система успешно сохраняет действие пользователя.
#### Описание
1. Пользователь ставит лайк.
2. Сайт отслеживает событие "like" и передает метаданные события в систему.
3. Система обрабатывает событие пользователя по переданным метаданным.
4. Система сохраняет пользовательское событие.

