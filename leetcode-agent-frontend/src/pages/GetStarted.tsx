import { useEffect } from "react";
import { API_BASE_URL } from "../config";

interface Props {
    onNext: () => void;
}

export default function GetStarted({ onNext }: Props) {


    useEffect(() => {
        chrome.storage.local.get(["authed", "token"], (res) => {
            if (res.authed && res.token) onNext();
        });
    }, []);

    const handleAuth = async () => {
        chrome.identity.launchWebAuthFlow(
            {
                url: `${API_BASE_URL}/auth/github`,
                interactive: true
            },
            (redirectUrl) => {
                if (chrome.runtime.lastError || !redirectUrl) {
                    console.error("❌ Auth failed:", chrome.runtime.lastError);
                    return;
                }

                // Example: https://<EXT_ID>.chromiumapp.org/provider_cb?username=foo&email=bar&token=xyz
                const url = new URL(redirectUrl);
                console.log("URL:", url);
                const token = url.searchParams.get("token");
                const username = url.searchParams.get("username");
                const email = url.searchParams.get("email");
                const avatar_url = url.searchParams.get("avatar_url");

                if (!token) {
                    console.error("❌ No token found in redirect");
                    return;
                }

                const user = { username, email, avatar_url };

                chrome.storage.local.set(
                    { authed: true, token, user },
                    () => {
                        console.log("✅ Stored user:", user);
                        onNext();
                    }
                );
            }
        );
    };


    return (
        <div className="p-4 w-72">
            <h1 className="text-lg font-bold mb-4">Welcome to LeetCode Agent</h1>
            <button
                onClick={handleAuth}
                className="bg-green-500 hover:bg-blue-600 text-white px-3 py-2 rounded w-full"
            >
                Get Started
            </button>
        </div>
    );
}
