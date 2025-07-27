📌 What is NEAT?
NEAT is an evolutionary algorithm that evolves artificial neural networks (ANNs). It starts with minimal structure and gradually complexifies networks over generations through:

Reproduction (sexual or asexual)

Mutation (adding new nodes and connections)

A user-defined fitness function scores each genome (individual ANN) based on how well it solves the problem. Over generations, fitter genomes survive and evolve, enabling the algorithm to discover increasingly complex and effective solutions.

The evolution stops when:

A genome reaches a user-defined fitness threshold, or

The maximum number of generations is reached.

🎮 Games
🐦 Flappy Bird AI
"Not the best version of the game—but the goal was AI, not polish!"

<img width="545" height="981" alt="Flappy Bird" src="https://github.com/user-attachments/assets/fd7469d3-b805-4e7a-81c5-b788498549b2" />
In this version, NEAT is used to teach the bird how to fly between pipes without crashing. Over generations, birds learn to jump with better timing.

🦖 T-Rex Runner AI
Inspired by this great tutorial by Max Rohowsky:
🔗 Watch the playlist

<img width="1068" height="561" alt="Trex Runner 1" src="https://github.com/user-attachments/assets/0987a01a-5add-4f8c-8d10-e2df2166c6b0" /> <img width="1059" height="544" alt="Trex Runner 2" src="https://github.com/user-attachments/assets/a1178f70-74e2-41c2-a412-4357b8611678" />
Here, the dino learns to jump over cacti and dodge flying obstacles. NEAT evolves agents that can survive longer and adapt to faster speeds.

⚙️ How It Works
Each game uses NEAT to simulate generations of AI agents.

A fitness function defines success (e.g., distance traveled, points scored).

NEAT evolves better-performing agents over time.

Neural networks increase in complexity via structural mutations (new nodes/connections).

📁 Credits & Acknowledgments
Game development based on YouTube tutorials.

NEAT algorithm implemented manually by me.

Thanks to Max Rohowsky for the T-Rex game tutorial inspiration.

🚧 Notes
These projects are more about AI learning than perfect gameplay or visuals.

Feel free to fork, modify, or use as a starting point for your own NEAT-based projects.

