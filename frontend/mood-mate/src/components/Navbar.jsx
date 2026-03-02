import React from "react";

export default function Navbar() {
  return (
    <nav className="fixed top-0 left-0 w-full z-50 backdrop-blur-xl bg-[#111827]/70 border-b border-white/10">
      
      <div className="max-w-7xl mx-auto px-6 md:px-12 py-5 flex justify-between items-center">
        
        {/* Logo */}
        <h1 className="text-2xl font-extrabold tracking-tight bg-gradient-to-r from-pink-400 via-purple-400 to-indigo-400 bg-clip-text text-transparent">
          <a href="/">
          AIMoodMate
          </a>
        </h1>

        {/* Nav Links */}
        <div className="hidden md:flex items-center space-x-10 text-gray-300 font-medium">
          
          <a 
            href="/" 
            className="relative group hover:text-white transition duration-300"
          >
            Home
            <span className="absolute left-0 -bottom-1 w-0 h-[2px] bg-pink-400 transition-all duration-300 group-hover:w-full"></span>
          </a>

          <a 
            href="/features" 
            className="relative group hover:text-white transition duration-300"
          >
            Features
            <span className="absolute left-0 -bottom-1 w-0 h-[2px] bg-purple-400 transition-all duration-300 group-hover:w-full"></span>
          </a>

          <a 
            href="/about" 
            className="relative group hover:text-white transition duration-300"
          >
            About
            <span className="absolute left-0 -bottom-1 w-0 h-[2px] bg-indigo-400 transition-all duration-300 group-hover:w-full"></span>
          </a>

        </div>

        {/* CTA Button */}
        <button className="hidden md:block px-6 py-2 rounded-xl bg-gradient-to-r from-pink-500 to-purple-500 text-white font-semibold shadow-lg hover:scale-105 transition duration-300">
          Get Started
        </button>
      </div>
    </nav>
  );
}