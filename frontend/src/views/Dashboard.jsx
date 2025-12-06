import { useEffect, useState } from 'react';
import axios from 'axios';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';
import { Activity, GitCommit, FileText, Zap } from 'lucide-react';

const StatCard = ({ icon: Icon, label, value, color }) => (
    <div className="glass p-6 rounded-2xl border-l-4" style={{ borderColor: color }}>
        <div className="flex items-start justify-between">
            <div>
                <p className="text-gray-400 text-sm font-medium">{label}</p>
                <h3 className="text-3xl font-bold mt-2">{value}</h3>
            </div>
            <div className="p-3 rounded-lg bg-white/5">
                <Icon size={24} style={{ color }} />
            </div>
        </div>
    </div>
);

export default function Dashboard({ projectId }) {
    const [metrics, setMetrics] = useState({
        totalFiles: 0,
        avgComplexity: 0,
        topFunctions: [],
        issuesCount: 0,
        gitCommits: '-'
    });

    useEffect(() => {
        // Fetch real data
        axios.get(`${import.meta.env.VITE_API_URL || 'http://localhost:8000'}/api/analyze/python/${projectId}`)
            .then(res => {
                const { complexity, nodes } = res.data;
                const fileMetrics = complexity.file_metrics || {};

                // Transform data for chart
                const chartData = Object.entries(fileMetrics).map(([name, score]) => ({
                    name: name.split('\\').pop().split('/').pop(), // Basename
                    value: score
                })).slice(0, 5); // Top 5

                setMetrics({
                    totalFiles: Object.keys(fileMetrics).length || nodes.length, // Fallback
                    avgComplexity: complexity.average_complexity ? complexity.average_complexity.toFixed(2) : 'N/A',
                    topFunctions: chartData,
                    issuesCount: res.data.issues ? res.data.issues.count : 0,
                    gitCommits: res.data.git_stats ? res.data.git_stats.commits : 'N/A'
                });
            })
            .catch(e => console.error(e));
    }, [projectId]);

    return (
        <div className="space-y-8">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                <StatCard icon={FileText} label="Total Files Analyzed" value={metrics.totalFiles} color="#38bdf8" />
                <StatCard icon={Activity} label="Avg Complexity" value={metrics.avgComplexity} color="#f472b6" />
                <StatCard icon={Zap} label="Issues Detected" value={metrics.issuesCount} color="#fbbf24" />
                <StatCard icon={GitCommit} label="Git Commits" value={metrics.gitCommits} color="#a78bfa" />
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                <div className="glass p-8 rounded-2xl">
                    <h3 className="text-xl font-bold mb-6">Complexity Overview</h3>
                    <div className="h-[300px]">
                        <ResponsiveContainer width="100%" height="100%">
                            <BarChart data={metrics.topFunctions}>
                                <XAxis dataKey="name" stroke="#94a3b8" />
                                <YAxis stroke="#94a3b8" />
                                <Tooltip
                                    contentStyle={{ backgroundColor: '#1e293b', border: 'none', borderRadius: '8px' }}
                                    itemStyle={{ color: '#fff' }}
                                />
                                <Bar dataKey="value" fill="#38bdf8" radius={[4, 4, 0, 0]} />
                            </BarChart>
                        </ResponsiveContainer>
                    </div>
                </div>

                <div className="glass p-8 rounded-2xl">
                    <h3 className="text-xl font-bold mb-6">Recent Activity</h3>
                    <div className="space-y-4">
                        {[1, 2, 3].map((i) => (
                            <div key={i} className="flex items-center gap-4 p-3 hover:bg-white/5 rounded-lg transition-colors">
                                <div className="w-2 h-2 rounded-full bg-green-400"></div>
                                <div className="flex-1">
                                    <p className="font-medium text-sm">Analysis Completed</p>
                                    <p className="text-xs text-gray-500">Just now</p>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            </div>
        </div>
    );
}
