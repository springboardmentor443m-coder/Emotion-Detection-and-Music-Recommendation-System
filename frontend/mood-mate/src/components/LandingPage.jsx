import React from "react";
import Navbar from "./Navbar";
import {useNavigate} from 'react-router-dom';


export default function LandingPage() {
  const navigate = useNavigate();
  return (
    <div className="min-h-screen bg-[#0f172a] text-white selection:bg-pink-500/30 overflow-x-hidden relative">

      {/* Animated Background Glow */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-[-10%] left-[-10%] w-[500px] h-[500px] bg-purple-600/20 rounded-full blur-[120px] animate-pulse"></div>
        <div className="absolute bottom-[-10%] right-[-10%] w-[600px] h-[600px] bg-indigo-600/20 rounded-full blur-[120px] animate-pulse delay-1000"></div>
      </div>

      <Navbar />

      <main className="relative z-10 mt-0">

        {/* HERO SECTION */}
        <section className="container mx-auto px-6 md:px-12 pt-28 pb-24 flex flex-col lg:flex-row items-center gap-16">

          {/* Left Content */}
          <div className="flex-1 text-center lg:text-left space-y-8">

            <div className="inline-block px-5 py-2 rounded-full bg-white/5 border border-white/10 text-indigo-300 text-sm tracking-wider uppercase">
              ✨ AI for emotional clarity
            </div>

            <h1 className="text-5xl md:text-7xl font-extrabold leading-[1.1] tracking-tight">
              Your Intelligent <br />
              <span className="bg-gradient-to-r from-pink-400 via-purple-400 to-indigo-400 bg-clip-text text-transparent animate-gradient">
                Mood Companion
              </span>
            </h1>

            <p className="text-lg md:text-xl text-gray-400 max-w-xl mx-auto lg:mx-0">
              Experience emotionally aware AI that understands your patterns,
              supports your growth, and helps you build lasting resilience.
            </p>

            <div className="flex flex-col sm:flex-row items-center justify-center lg:justify-start gap-4">
              <button onClick={()=>navigate("/features")} className="px-8 py-4 bg-white text-black font-bold rounded-2xl hover:bg-pink-500 hover:text-white transition-all duration-300 shadow-xl shadow-white/10">
                Start Your Journey
              </button>

              <button className="px-8 py-4 bg-white/5 border border-white/10 rounded-2xl font-semibold hover:bg-white/10 transition-all">
                How it works
              </button>
            </div>
          </div>

          {/* Right Dynamic Glass UI Mock */}
          <div className="flex-1 relative">

            <div className="absolute inset-0 bg-gradient-to-tr from-pink-500/20 to-purple-500/20 blur-3xl rounded-[3rem] animate-pulse"></div>

            <div className="relative p-10 rounded-[3rem] bg-white/5 border border-white/10 backdrop-blur-2xl shadow-2xl">

              <div className="space-y-6">

                <div className="p-4 rounded-2xl bg-white/5 border border-white/10">
                  <p className="text-sm text-gray-400">Current Mood</p>
                  <div className="mt-2 h-3 w-full bg-white/10 rounded-full overflow-hidden">
                    <div className="h-full w-2/3 bg-gradient-to-r from-pink-400 to-purple-400 rounded-full animate-pulse"></div>
                  </div>
                </div>

                <div className="p-4 rounded-2xl bg-white/5 border border-white/10">
                  <p className="text-sm text-gray-400">AI Insight</p>
                  <p className="mt-2 text-sm text-gray-300">
                    You’ve shown improved mood consistency this week.
                  </p>
                </div>

                <div className="p-4 rounded-2xl bg-gradient-to-r from-pink-500/20 to-purple-500/20 border border-white/10">
                  <p className="text-sm font-semibold">
                    ✨ Suggested Action
                  </p>
                  <p className="text-sm text-gray-300 mt-1">
                    Try a 3-minute breathing session for balance.
                  </p>
                </div>

              </div>

            </div>
          </div>

        </section>

        {/* FEATURES SECTION */}
        <section className="container mx-auto px-6 md:px-12 py-24">

          <div className="text-center max-w-3xl mx-auto mb-20">
            <h2 className="text-3xl md:text-5xl font-bold mb-6">
              Designed for modern minds
            </h2>
            <p className="text-gray-400 text-lg">
              Powerful AI tools crafted to support your emotional intelligence journey.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">

            <FeatureCard
              icon="📊"
              title="Smart Tracking"
              desc="Log emotions effortlessly with a frictionless interface."
            />

            <FeatureCard
              icon="🧠"
              title="Neural Insights"
              desc="AI detects patterns and gives actionable recommendations."
            />

            <FeatureCard
              icon="🧘"
              title="Guided Growth"
              desc="Personalized exercises tailored to your mental state."
            />

          </div>

        </section>
      </main>

      <footer className="border-t border-white/5 py-12 text-center">
        <p className="text-gray-500 text-sm">
          © {new Date().getFullYear()} AIMoodMate. Crafted for clarity.
        </p>
      </footer>
    </div>
  );
}


// Feature Card
function FeatureCard({ icon, title, desc }) {
  return (
    <div className="group p-10 rounded-[2rem] bg-white/5 border border-white/10 backdrop-blur-xl hover:border-pink-400/40 transition-all duration-500 hover:-translate-y-2">

      <div className="text-4xl mb-6 transform group-hover:scale-110 transition duration-500">
        {icon}
      </div>

      <h3 className="text-xl font-bold mb-4 group-hover:text-pink-400 transition-colors">
        {title}
      </h3>

      <p className="text-gray-400 leading-relaxed text-sm md:text-base">
        {desc}
      </p>
    </div>
  );
}