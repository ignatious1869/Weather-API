# Weather-API
Class code for the weather API
Project Overview
This project implements a two-node forecasting system that connects a local client to a remote service to exchange weather data through the Internet. This will demonstrate distributed communication, fault tolerance, and basic security between a client and a server.
This project implements a two-node Distributed Weather Forecasting System using Python 3.
It demonstrates distributed communication, fault tolerance, and basic security between a client and a server.
System Design
The system has two independent nodes, the client and the server, that communicate through TCP sockets. The client sends a request with a city name and a shared key and then receives the average temperature of that city. The server listens for incoming requests, verifies the key, calls the API and then returns the results to the client. While the client and server are communicating, they’re logging all the communication and events with timestamps to log files.
Network Configuration 
We used TCP sockets with a shared key jwu2025 for basic authentication with both nodes using the port 5050. Both the server and client python files record everything to .txt files that record the API events and the connections and responses.
When the client requests a temperature of a certain city, our server calls the Open-Meteo Geocoding API to convert the city name into latitude and longitude. It then calls the Forecast API to receive the hourly temperature of the next 24 hours. We then average the temperature and return the average temperature of that city in Celsius.

Fault Tolerance
* We have it set up that if you misspell or provide an invalid city that the server sends the client an “Error retrieving data” message so the client knows their results couldn’t be provided.
*  If the client uses the wrong shared key, the server will deny access and close the connection.
* If there’s a disconnection or the server isn’t running before the client tries to access information, the client will see “Server unavailable, retrying…” Once the server is up and running, the client will be able to reconnect and request the temperature of a city.
________________


Reflection Questions
1. Our project demonstrates several key distributed systems concepts from Coulouris, including client–server communication, transparency, and fault tolerance. The client and server exchange data over a network connection which shows how distributed nodes interact remotely. The system also hides the complexity of the API from the client which represents transparency in distribution. We implemented basic reliability and authentication features to show how middleware helps maintain secure and dependable communication between components. Logging on both sides also supports observability, which is another important concept discussed in the textbook.
2. We handled communication reliability mainly through retries and error handling. If the server isn’t available the client automatically retries the connection after a few seconds instead of crashing. The server also responds with specific error messages when the API fails or when the shared key is incorrect so the client knows what went wrong. Every event is logged with a timestamp so we can track when issues occur and how the system responds. This setup made it easier to test recovery behavior and confirm that the client could reconnect once the server was back online.
3. To scale this for multiple clients and regions we could modify the server to handle multiple clients at once, using threads or asynchronous I/O. We could also use multiple servers and use a load balancer to spread out the connections. Adding caching would help reduce repeated API calls, and using cloud services would make it easier to support users in different regions. These upgrades would let the system handle more requests efficiently without losing performance or reliability.
4. We learned that distributed systems are more unpredictable and complicated than they seem. Even though the client sees a simple process, there’s a lot going on behind the scenes, network delays, failed connections, and API timeouts. Real systems need built-in recovery and logging so that problems can be identified and fixed quickly. This lab showed us how important transparency and fault tolerance are when designing real-world distributed applications.
