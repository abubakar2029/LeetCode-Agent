import json
import os
from app.utils.github_client import run_query

def save_to_file(data, filename="repo_tree.json"):
    filepath = os.path.join(os.getcwd(), filename)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    return {"message": f"Saved to {filepath}"}


def get_repo_tree(owner: str, repo: str, branch: str = "main", token: str = None, save: bool = True):
    """
    Fetch repo tree (3 levels deep).
    Pass user's decrypted GitHub token for private repos.
    """
    query = """
    query($owner: String!, $repo: String!, $branch: String!) {
      repository(owner: $owner, name: $repo) {
        object(expression: $branch) {
          ... on Tree {
            entries {
              name
              type
              object {
                ... on Tree {
                  entries {
                    name
                    type
                    object {
                      ... on Tree {
                        entries {
                          name
                          type
                        }
                      }
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
    """
    result = run_query(query, {"owner": owner, "repo": repo, "branch": branch + ":"}, token)

    if save:
        save_to_file(result, f"{repo}_tree.json")

    return result


def get_commit_history(owner: str, repo: str, path: str, branch: str = "main", last: int = 5, token: str = None):
    query = """
    query($owner: String!, $repo: String!, $branch: String!, $path: String!, $last: Int!) {
      repository(owner: $owner, name: $repo) {
        object(expression: $branch) {
          ... on Commit {
            history(first: $last, path: $path) {
              edges {
                node {
                  message
                  committedDate
                  author {
                    name
                  }
                  url
                }
              }
            }
          }
        }
      }
    }
    """
    return run_query(query, {"owner": owner, "repo": repo, "branch": branch, "path": path, "last": last}, token)
