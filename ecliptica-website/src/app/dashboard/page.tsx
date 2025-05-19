"use client";

import React, { useState, useEffect } from "react";
import {
  Folder, FileText, Clock, Sun, Moon,
  ChevronDown, LogOut, Plus
} from "lucide-react";
import Link from "next/link";
import { LayoutDashboard, User } from "lucide-react";
import { toast, ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

interface Project {
  name: string;
  keywords: string;
  createdAt: string;
  path: string;
}

export default function Dashboard() {
  const [username, setUsername] = useState("");
  const [projects, setProjects] = useState<Project[]>([]);
  const [darkMode, setDarkMode] = useState(true);
  const [showDropdown, setShowDropdown] = useState(false);
  const [loading, setLoading] = useState(false);
  const [showAll, setShowAll] = useState(false); // NEW

  useEffect(() => {
    const storedName = localStorage.getItem("ecliptica_username") || "User";
    setUsername(storedName);

    const storedProjects = localStorage.getItem("ecliptica_projects");
    if (storedProjects) {
      setProjects(JSON.parse(storedProjects));
    }
  }, []);

  const handleLogout = () => {
    localStorage.removeItem("ecliptica_username");
    window.location.href = "/";
  };

  const handleCreateProject = async () => {
    setLoading(true);
    try {
      const response = await fetch("http://127.0.0.1:5000/run_ctm", {
        method: "POST",
      });

      if (!response.ok) throw new Error("Backend error");

      const blob = await response.blob();
      const contentDisposition = response.headers.get("Content-Disposition");
      const fileName = contentDisposition?.split("filename=")[1]?.replaceAll('"', "") || "outputs.zip";
      const zipUrl = URL.createObjectURL(blob);

      const downloadLink = document.createElement("a");
      downloadLink.href = zipUrl;
      downloadLink.download = fileName;
      downloadLink.click();
      URL.revokeObjectURL(zipUrl);

      const newProject: Project = {
        name: fileName.replace(".zip", ""),
        keywords: "N/A",
        createdAt: new Date().toLocaleString(),
        path: `/outputs/${fileName}`,
      };

      const updatedProjects = [newProject, ...projects];
      setProjects(updatedProjects);
      localStorage.setItem("ecliptica_projects", JSON.stringify(updatedProjects));
    } catch (error) {
      console.error("Error:", error);
      alert("Something went wrong. Make sure the backend is running.");
    } finally {
      setLoading(false);
    }
  };

  const handleDownloadNotice = (project: Project) => {
    toast.success(`${project.name} has been downloaded! You can find it in your Downloads folder.`, {
      position: "bottom-right",
      autoClose: 5000,
      theme: darkMode ? "dark" : "light",
    });
  };

  return (
    <>
      <div className={`min-h-screen font-sans flex transition-colors duration-500 ${darkMode ? "bg-[#0f172a] text-white" : "bg-white text-black"}`}>
        {/* Sidebar */}
        <aside className="w-64 min-h-screen bg-[#007698] text-white p-6 space-y-6 fixed top-0 left-0">
          <Link href="/">
            <div className="flex items-center space-x-2 mb-6 cursor-pointer">
              <img src="/imgs/logo.jpg" alt="Ecliptica Logo" className="w-14 h-14 rounded" />
              <span className="text-2xl font-semibold tracking-wide">Ecliptica</span>
            </div>
          </Link>

          <div className="text-sm font-semibold text-[#d4ecff] uppercase tracking-widest mb-2">Menu</div>
          <nav className="space-y-4">
            <Link href="/dashboard" className="flex items-center space-x-3 text-white hover:text-[#60a5fa] transition">
              <LayoutDashboard className="w-5 h-5" />
              <span className="text-base font-medium">Dashboard</span>
            </Link>
            <Link href="/profile" className="flex items-center space-x-3 text-white hover:text-[#60a5fa] transition">
              <User className="w-5 h-5" />
              <span className="text-base font-medium">Profile</span>
            </Link>
          </nav>
        </aside>

        {/* Main content */}
        <div className="ml-64 flex-1 px-10 py-10">
          <div className="flex justify-between items-center mb-8">
            <h1 className="text-4xl font-bold tracking-wide">Welcome {username}!</h1>
            <div className="flex items-center space-x-4 relative">
              <button onClick={() => setDarkMode(!darkMode)} className="p-2 rounded-full border hover:bg-gray-200 dark:hover:bg-gray-700 transition">
                {darkMode ? <Sun className="w-5 h-5" /> : <Moon className="w-5 h-5" />}
              </button>
              <div className="relative">
                <button
                  onClick={() => setShowDropdown(!showDropdown)}
                  className={`flex items-center space-x-2 border px-3 py-1 rounded-full text-sm transition ${darkMode ? "text-white hover:bg-[#1e293b]" : "text-black hover:bg-gray-100"}`}
                >
                  <span>{username}</span>
                  <ChevronDown className="w-4 h-4" />
                </button>
                {showDropdown && (
                  <div className="absolute right-0 mt-2 w-40 bg-white dark:bg-[#1e293b] border border-gray-200 dark:border-gray-700 rounded-md shadow-md z-10">
                    <button
                      onClick={handleLogout}
                      className="flex items-center w-full px-4 py-2 text-sm text-black dark:text-white hover:bg-gray-100 dark:hover:bg-gray-700"
                    >
                      <LogOut className="w-4 h-4 mr-2" /> Log Out
                    </button>
                  </div>
                )}
              </div>
            </div>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-3 gap-6 mb-10">
            <Card title="Total Projects" value={projects.length.toString()} darkMode={darkMode} />
            <Card title="Most Common Keyword" value={projects.length > 0 ? getMostCommonKeyword(projects) : "N/A"} darkMode={darkMode} />
            <Card title="Latest Project" value={projects.length > 0 ? projects[0].name : "N/A"} darkMode={darkMode} />
          </div>

          <div className={`rounded-xl p-6 shadow transition-colors duration-300 ${darkMode ? "bg-[#1e293b] text-white" : "bg-gray-100 text-black"}`}>
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-2xl font-semibold">Recent Projects</h2>
              <button
                onClick={handleCreateProject}
                disabled={loading}
                className="flex items-center space-x-2 bg-[#007698] text-white px-4 py-2 rounded-full hover:bg-blue-600 transition text-sm disabled:opacity-60"
              >
                <Plus className="w-4 h-4" />
                <span>{loading ? "Processing..." : "Create New Project"}</span>
              </button>
            </div>

            {loading && (
              <div className="flex justify-center items-center mb-4">
                <div className="animate-spin rounded-full h-6 w-6 border-t-4 border-blue-500"></div>
                <span className="ml-4 text-blue-600">Generating outputs…</span>
              </div>
            )}

            <ul className="space-y-4">
              {(showAll ? projects : projects.slice(0, 4)).map((project, index) => (
                <li
                  key={index}
                  className={`flex items-center justify-between rounded-lg p-4 transition duration-300 ${darkMode ? "bg-[#334155]" : "bg-white border border-gray-200"}`}
                >
                  <div className="flex items-center space-x-4">
                    <Folder className="text-yellow-400" />
                    <div>
                      <h3 className="text-lg font-medium">{project.name}</h3>
                      <p className="text-sm text-gray-400">
                        <FileText className="inline-block w-4 h-4 mr-1" /> {project.keywords} | <Clock className="inline-block w-4 h-4 mx-1" /> {project.createdAt}
                      </p>
                    </div>
                  </div>
                  <button
                    onClick={() => handleDownloadNotice(project)}
                    className="bg-[#007698] text-white px-4 py-2 rounded-full hover:bg-blue-600 text-sm transition"
                  >
                    Download
                  </button>
                </li>
              ))}
            </ul>

            {projects.length > 4 && (
              <div className="text-center mt-4">
                <button
                  onClick={() => setShowAll(!showAll)}
                  className="text-blue-600 hover:underline font-medium"
                >
                  {showAll ? "View Less" : "View All Projects"}
                </button>
              </div>
            )}
          </div>
        </div>
      </div>
      <ToastContainer />
    </>
  );
}

const Card = ({ title, value, darkMode }: { title: string, value: string, darkMode: boolean }) => (
  <div className={`rounded-xl p-6 shadow transition-colors duration-300 ${darkMode ? "bg-[#1e293b] text-white" : "bg-gray-100 text-black"}`}>
    <h2 className="text-lg font-medium mb-2">{title}</h2>
    <p className="text-2xl font-bold">{value}</p>
  </div>
);

function getMostCommonKeyword(projects: Project[]) {
  const freq: Record<string, number> = {};
  for (const project of projects) {
    const keyword = project.keywords;
    freq[keyword] = (freq[keyword] || 0) + 1;
  }
  return Object.entries(freq).sort((a, b) => b[1] - a[1])[0]?.[0] || "N/A";
}
