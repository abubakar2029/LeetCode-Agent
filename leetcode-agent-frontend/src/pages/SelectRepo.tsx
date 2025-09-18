import { API_BASE_URL } from "../config";

import { useEffect, useState } from "react";

interface Props {
  onNext: () => void;
}

export default function SelectRepo({ onNext }: Props) {
  const [repos, setRepos] = useState<string[]>([]);

  useEffect(() => {
    chrome.storage.local.get("token", async ({ token }) => {
      const res = await fetch(`${API_BASE_URL}/github/repos`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      const data = await res.json();
      setRepos(data.repos || []);
    });
  }, []);


  const handleSelect = async (repo: string) => {
    chrome.storage.local.get("token", async ({ token }) => {
      await fetch(`${API_BASE_URL}/github/select_repo?repo_name=${repo}`, {
        method: "POST",
        headers: { Authorization: `Bearer ${token}` },
      });
      chrome.storage.local.set({ repo }, () => onNext());
    });
  };

  return (
    <div className="p-4 w-72">
      <h2 className="text-lg font-bold mb-3">Select a Repository</h2>
      <ul className="space-y-2">
        {repos.map((repo, i) => (
          <li key={i}>
            <button
              onClick={() => handleSelect(repo)}
              className="w-full text-left p-2 bg-gray-100 hover:bg-gray-200 rounded"
            >
              {repo}
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}
