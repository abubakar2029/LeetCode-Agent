import { API_BASE_URL } from "../config";

import { useEffect, useState } from "react";

interface Problem {
    title: string;
    url: string;
}

export default function TodayProblem() {
    const [problem, setProblem] = useState<Problem | null>(null);

    useEffect(() => {
        fetch(`${API_BASE_URL}/problem/today`)
            .then((res) => res.json())
            .then((data: Problem) => setProblem(data))
            .catch(() =>
                setProblem({
                    title: "Two Sum",
                    url: "https://leetcode.com/problems/two-sum",
                })
            );
    }, []);

    if (!problem) return <div className="p-4">Loading...</div>;

    return (
        <div className="p-4 w-72">
            <h2 className="text-lg font-bold mb-2">Today's Problem</h2>
            <a href={problem.url} target="_blank" rel="noreferrer" className="text-blue-600 underline">
                {problem.title}
            </a>
            <p className="mt-3 text-sm italic text-gray-600">
                “Consistency beats intensity — one problem a day builds mastery.”
            </p>
        </div>
    );
}
