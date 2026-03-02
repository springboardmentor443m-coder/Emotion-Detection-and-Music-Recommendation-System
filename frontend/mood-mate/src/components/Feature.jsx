import React from "react";
import Navbar from "./Navbar";
import { Brain, Sparkles, Music } from "lucide-react";

export default function FeaturesPage() {
  return (
    <div className="min-h-screen bg-[#0f172a] text-white overflow-x-hidden relative">

      {/* Background Glow */}
      <div className="fixed inset-0 pointer-events-none">
        <div className="absolute top-[-10%] left-[-10%] w-[500px] h-[500px] bg-purple-600/20 rounded-full blur-[120px] animate-pulse"></div>
        <div className="absolute bottom-[-10%] right-[-10%] w-[600px] h-[600px] bg-pink-600/20 rounded-full blur-[120px] animate-pulse" style={{ animationDelay: "2s" }}></div>
      </div>

      <Navbar />

      <main className="relative z-10 pt-32 px-6 md:px-12">

        {/* Section Heading */}
        <div className="text-center max-w-3xl mx-auto mb-20">
          <h2 className="text-4xl md:text-6xl font-extrabold bg-gradient-to-r from-pink-400 via-purple-400 to-indigo-400 bg-clip-text text-transparent">
            Smart Features for a Better You
          </h2>
          <p className="text-gray-400 mt-6 text-lg">
            Personalized AI tools designed to elevate your emotional well-being.
          </p>
        </div>

        {/* Feature Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-10">

          {/* Mood Prediction */}
          <FeatureCard
            icon={<Brain size={40} />}
            title="Mood Prediction"
            description="Our AI analyzes your patterns and predicts emotional shifts before they happen, helping you stay prepared and balanced."
            gradient="from-pink-500 to-purple-500"
          />

          {/* Yoga Insights */}
          <FeatureCard
            icon={<Sparkles size={40} />}
            title="Yoga Insights"
            description="Receive personalized yoga and breathing exercises based on your emotional state to restore inner harmony."
            gradient="from-purple-500 to-indigo-500"
          />

          {/* Music Recommendation */}
          <FeatureCard
            icon={<Music size={40} />}
            title="Music Recommendation"
            description="Get curated playlists that align with your current mood — relax, energize, or refocus instantly."
            gradient="from-indigo-500 to-pink-500"
          />

        </div>
      </main>
    </div>
  );
}


/* Reusable Feature Tile */
function FeatureCard({ icon, title, description, gradient }) {
  return (
    <div className="group relative p-10 rounded-[2rem] bg-white/5 border border-white/10 backdrop-blur-xl transition-all duration-500 hover:-translate-y-3 hover:border-white/20">
      
      {/* Hover Glow */}
      <div className={`absolute inset-0 opacity-0 group-hover:opacity-100 transition duration-500 rounded-[2rem] bg-gradient-to-br ${gradient} blur-2xl -z-10`}></div>

      {/* Icon */}
      <div className={`mb-6 inline-flex p-4 rounded-2xl bg-gradient-to-r ${gradient}`}>
        {icon}
      </div>

      {/* Title */}
      <h3 className="text-2xl font-bold mb-4 group-hover:text-white transition-colors">
        {title}
      </h3>

      {/* Description */}
      <p className="text-gray-400 leading-relaxed">
        {description}
      </p>
    </div>
  );
}