      [ API / Producer ]
               |
               v
      ┌────────────────┐
      |   RabbitMQ     |
      |   Queue: orders|
      └────────────────┘
               |
               v
     [ Worker / Consumer ]
