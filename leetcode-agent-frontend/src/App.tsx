import { useEffect, useState } from 'react'
// import reactLogo from './assets/react.svg'
// import viteLogo from '/vite.svg'
import './App.css'
import GetStarted from './pages/GetStarted';
import SelectRepo from './pages/SelectRepo';
import TodayProblem from './pages/TodayProblem';

type View = "loading" | "getstarted" | "selectrepo" | "today";

export function App() {
  const [view, setView] = useState<View>("loading");

  useEffect(() => {
    chrome.storage.local.get(["authed", "repo"], (result) => {
      if (!result.authed) setView("getstarted");
      else if (!result.repo) setView("selectrepo");
      else setView("today");
    });
  }, []);

  if (view === "loading") return <div className="p-4">Loading...</div>;
  if (view === "getstarted") return <GetStarted onNext={() => setView("selectrepo")} />;
  if (view === "selectrepo") return <SelectRepo onNext={() => setView("today")} />;
  if (view === "today") return <TodayProblem />;
}

export default App;
