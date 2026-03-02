import React from "react";
import Navbar from "./Navbar";

const About = () => {
  return (
    <div className="min-h-screen bg-[#0f172a] text-white overflow-x-hidden relative">

      {/* Animated Background Glow */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-[-10%] left-[-10%] w-[500px] h-[500px] bg-purple-600/20 rounded-full blur-[120px] animate-pulse"></div>
        <div className="absolute bottom-[-10%] right-[-10%] w-[600px] h-[600px] bg-indigo-600/20 rounded-full blur-[120px] animate-pulse delay-1000"></div>
      </div>

      <Navbar />

      <main className="relative z-10">

        {/* Hero Section */}
        <section className="text-center py-20 px-6 mt-10">
          <h1 className="text-5xl md:text-6xl font-extrabold mb-6">
            About{" "}
            <span className="bg-gradient-to-r from-pink-400 via-purple-400 to-indigo-400 bg-clip-text text-transparent">
              AIMoodMate
            </span>
          </h1>
          <p className="text-lg text-gray-400 max-w-3xl mx-auto">
            AIMoodMate is an AI-powered Emotion Detection and Music Recommendation 
            System that understands how you feel and curates the perfect music 
            experience to match or uplift your mood.
          </p>
        </section>

        {/* Objective */}
        <section className="max-w-6xl mx-auto px-6 py-12">
          <div className="bg-white/5 border border-white/10 backdrop-blur-xl rounded-[2rem] p-10 shadow-xl">
            <h2 className="text-2xl font-bold mb-4 text-pink-400">
              🎯 Our Objective
            </h2>
            <p className="text-gray-400 leading-relaxed">
              The goal of AIMoodMate is to develop an intelligent system that detects 
              a user's emotional state through facial expressions or text input 
              using advanced AI/ML techniques. Based on the detected emotion, 
              the system recommends music that aligns with the mood or enhances 
              the user's emotional well-being.
            </p>
          </div>
        </section>

        {/* How It Works */}
        <section className="max-w-6xl mx-auto px-6 py-16">
          <h2 className="text-4xl font-bold text-center mb-16">
            How It Works
          </h2>

          <div className="grid md:grid-cols-3 gap-8">

            <GlassCard
              title="1️⃣ Emotion Detection"
              desc="Computer vision models analyze facial expressions while NLP processes text input to detect emotions like happiness, sadness, anger, or excitement."
            />

            <GlassCard
              title="2️⃣ AI Processing"
              desc="Machine learning models classify emotional states using trained datasets and feature extraction techniques for high accuracy."
            />

            <GlassCard
              title="3️⃣ Music Recommendation"
              desc="A smart recommendation engine suggests personalized songs that match or elevate your mood."
            />

          </div>
        </section>

        {/* Key Features */}
        <section className="max-w-6xl mx-auto px-6 py-12">
          <div className="bg-white/5 border border-white/10 backdrop-blur-xl rounded-[2rem] p-10">
            <h2 className="text-2xl font-bold mb-8 text-purple-400">
              ✨ Key Features
            </h2>

            <ul className="grid md:grid-cols-2 gap-6 text-gray-400">
              <li>✔ Real-time facial emotion recognition</li>
              <li>✔ Text-based sentiment analysis</li>
              <li>✔ AI-driven music recommendation engine</li>
              <li>✔ Personalized user experience</li>
              <li>✔ Clean and interactive UI</li>
              <li>✔ Scalable AI architecture</li>
            </ul>
          </div>
        </section>

        {/* Tech Stack */}
        <section className="max-w-6xl mx-auto px-6 py-16 text-center">
          <h2 className="text-4xl font-bold mb-16">
            🛠 Tech Stack
          </h2>

          <div className="grid md:grid-cols-3 gap-8">

            <GlassCard
              title="Frontend"
              desc="React.js, Tailwind CSS"
            />

            <GlassCard
              title="Backend"
              desc="Node.js / Flask API"
            />

            <GlassCard
              title="AI/ML"
              desc="CNN for emotion detection, NLP sentiment analysis, Recommendation algorithms"
            />

          </div>
        </section>

        {/* Vision */}
        <section className="py-20 text-center bg-gradient-to-r from-pink-500/10 to-purple-500/10 border-t border-white/10">
          <h2 className="text-4xl font-bold mb-6">
            💡 Our Vision
          </h2>
          <p className="max-w-3xl mx-auto text-gray-400 text-lg">
            We envision a world where technology understands human emotions 
            and enhances mental well-being through intelligent personalization. 
            AIMoodMate is a step toward emotionally aware AI systems.
          </p>
        </section>

      </main>

      <footer className="border-t border-white/5 py-12 text-center">
        <p className="text-gray-500 text-sm">
          © {new Date().getFullYear()} AIMoodMate. Crafted for clarity.
        </p>
      </footer>

    </div>
  );
};

export default About;


/* Reusable Glass Card */
function GlassCard({ title, desc }) {
  return (
    <div className="p-8 rounded-[2rem] bg-white/5 border border-white/10 backdrop-blur-xl hover:border-pink-400/40 transition-all duration-500 hover:-translate-y-2">
      <h3 className="text-xl font-bold mb-4 text-pink-400">
        {title}
      </h3>
      <p className="text-gray-400 leading-relaxed">
        {desc}
      </p>
    </div>
  );
}