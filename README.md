# Using Message Driven Architecture with RabbitMQ

This project implements a two-step payment process using a message queue service such as RabbitMQ. We are working on a payment app that allows students to pay tuition fees.

Message Driven Architecture (MDA) is an application architecture approach that enables software components to use messages to communicate with each other. MDA adopts an event-driven and asynchronous approach, which makes the application more flexible, scalable and resilient. Here are the basic components of MDA and an explanation of how it works:

1. **Producer:** These are the components that create messages and send them to the message queue. These components are usually pieces of code that detect when a certain event has occurred or complete a certain operation.

2. **Message Queue:** It is a queue system where messages are stored and waiting to be consumed. Messages are sent asynchronously and kept in the queue sequentially. The queue enables communication between multiple producers and consumers.

3. **Consumer:** These are the components that receive and process messages from the queue. The consumer reads the incoming messages, processes them, and can then create an appropriate response or take another action.

4. **Event Broker:** It is a tool that brings message producers and consumers together and ensures the forwarding of messages. This is used to publish events and deliver them to subscribers.

RabbitMQ is a popular open source message queuing software for MDA. RabbitMQ implements the AMQP (Advanced Message Queuing Protocol) standard and provides secure, reliable and scalable message communication between distributed systems. The main features of RabbitMQ are:

- **Queue Management:** RabbitMQ offers a flexible structure to manage a large number of queues. Queues can be filtered and routed to monitor specific message types or senders.
  
- **Message Publishing and Subscription:** RabbitMQ enables communication between publishers who report that an event has occurred and consumers who subscribe to these events (subscribers).
  
- **Routing and Filtering:** RabbitMQ offers a variety of routing and filtering strategies that enable messages to be routed and filtered to specific consumers.
  
- **User Authentication and Security:** RabbitMQ provides security measures such as firewalls, user authentication, and encryption.

In this project, RabbitMQ can be used to manage students' payment transactions in a two-step process. When students are asked to pay, the payment request is sent to the RabbitMQ message queue. This request is forwarded to the payment service and processed. A response message is then generated when the payment transaction is completed, which can be used to notify the student that the payment was successful.

This way, the payment process can be managed asynchronously using RabbitMQ and MDA. This makes the application more flexible, scalable and reliable because dependencies between payment transactions and other transactions are reduced and network traffic is better managed.

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
