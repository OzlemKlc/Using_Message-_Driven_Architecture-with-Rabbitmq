# Using Message Driven Architecture with RabbitMQ

This project implements a two-step payment process using a message queue service such as RabbitMQ. We are working on a payment app that allows students to pay tuition fees.

## Requirements

- Python 3.11.3
-Flask
- Pika (Python client library for RabbitMQ)
- Docker (for using RabbitMQ)

## Setup

1. Create a virtual environment:

     ```bash
     python -m venv venv
     ```

2. Activate the virtual environment:

     -Windows:

         ```bash
         .\venv\Scripts\activate
         ```

     - Linux/Mac:

         ```bash
         source venv/bin/activate
         ```

3. Install the required libraries:

     ```bash
     pip install flask pika
     ```

4. Start the RabbitMQ Docker container (optional, if RabbitMQ will be used):

     ```bash
     docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:management
     ```

## Use

1. Start the Flask app:

     ```bash
     python payment_app.py
     ```

2. Send HTTP POST request to make payment:

     ```bash
     POST /v1/pay-tuition
     ```

     - Example usage:

         ```bash
         curl -X POST -H "Content-Type: application/json" -d '{"student_no": "S001", "term": "Spring2024"}' http://localhost:9090/v1/pay-tuition
         ```

3. Once the payment process is initiated, payment information will be sent to the RabbitMQ message queue.

4. Once the payment transaction is completed successfully or unsuccessfully, notifications will be sent to the RabbitMQ message queue.

## Video Presentation
 https://drive.google.com/file/d/1VQxHbrJ1PfVewd2oNJvyEKt3kERl-VAz/view?usp=sharing
