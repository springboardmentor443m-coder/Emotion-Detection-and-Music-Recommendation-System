import { Routes, Route } from "react-router-dom";
import LandingPage from "./components/LandingPage";
import FeaturesPage from "./components/Feature";
import About from "./components/About";

function App() {
  return (
    <Routes>
      <Route path="/" element={<LandingPage />} />
      <Route path="/features" element={<FeaturesPage/>}/>
      <Route path = "/about" element = {<About/>}/>
    </Routes>
  );
}

export default App;