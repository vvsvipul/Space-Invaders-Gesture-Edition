# 🕹️ Space-Invaders-Gesture-Edition

## 🚀 Overview

Welcome to the **Space-Invaders-Gesture-Edition**! This project takes the classic Space Invaders experience and amplifies it with an enhanced multiplayer server architecture. Dive into a robust, efficient, and thrilling gaming experience with seamless TCP connections, intelligent room management, precise synchronization, game state handling, and optimized performance.

## 🎯 Objective

To build a scalable and efficient multiplayer server that supports concurrent players, ensures fair gameplay, and delivers optimal performance.

## ✨ Key Features

### 1. Multiplayer Server Architecture
   - Established TCP connections.
   - Managed multiple clients concurrently using Python's socket module and multithreading.

### 2. Room Management
   - Create and join game rooms with unique room codes.
   - Maintain client lists, game start status, and client timings for each room.

### 3. Synchronization and Communication
   - Synchronized access to shared resources using threading locks.
   - Efficiently send messages to all clients in a room simultaneously.

### 4. Game State Handling
   - Simultaneous game initiation for all clients in a room.
   - Capture finish times, sort client timings, and broadcast results for fair ranking.

### 5. Performance Considerations
   - Minimized latency and ensured smooth gameplay through multithreading and efficient socket communication.
   - Frame Rendering and FPS:
     - ⏱️ Average Time to Render a Frame: 0.0292 seconds.
     - 🎮 Average FPS: 34.21.

## 🛠️ Installation Guide

1. **Clone the Repository**
   ```bash
   git clone (https://github.com/vvsvipul/Space-Invaders-Gesture-Edition/)
   cd Space-Invaders-Gesture-Edition
2. **Run the Server**
    ```bash
    python server.py
3. **Run the Client**
   ```bash
   python client.py

## 📚 Documentation
For detailed documentation, visit: https://tar-jackrabbit-c7f.notion.site/SUMMER-INTERSHIP-2024-11168030ad9e4e61a26664e2809a3951

## 🤝 Contributing
We welcome contributions to make this project even better! Whether you have suggestions, improvements, or bug fixes, feel free to fork the repository, create a branch, and submit a pull request. 
