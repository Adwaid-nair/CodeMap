import { useEffect, useState } from 'react';
import axios from 'axios';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

export default function DependencyView({ projectId }) {
    const [metrics, setMetrics] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        axios.get(`${import.meta.env.VITE_API_URL || 'http://localhost:8000'}/api/analyze/python/${projectId}`)
            .then(res => {
                const fileMetrics = res.data.complexity.file_metrics;
                const chartData = Object.entries(fileMetrics).map(([name, value]) => ({
                    name,
                    complexity: value
                }));
                setMetrics(chartData);
            })
            .catch(err => console.error(err))
            .finally(() => setLoading(false));
    }, [projectId]);

    return (
        <div className="space-y-6">
            <h2 className="text-2xl font-bold">File Complexity & Dependencies</h2>

            <div className="grid grid-cols-1 gap-6">
                <div className="glass p-8 rounded-2xl min-h-[500px] border border-white/10">
                    <h3 className="text-xl font-semibold mb-6">Complexity Overview</h3>
                    {loading ? (
                        <div className="animate-pulse text-gray-400">Loading metrics...</div>
                    ) : (
                        <div className="h-[400px] w-full">
                            {metrics && metrics.length > 0 ? (
                                <ResponsiveContainer width="100%" height="100%">
                                    <BarChart data={metrics}>
                                        <CartesianGrid strokeDasharray="3 3" stroke="#ffffff20" />
                                        <XAxis dataKey="name" stroke="#9ca3af" />
                                        <YAxis stroke="#9ca3af" />
                                        <Tooltip
                                            contentStyle={{ backgroundColor: '#1e293b', border: '1px solid #38bdf8' }}
                                        />
                                        <Legend />
                                        <Bar dataKey="complexity" fill="#38bdf8" />
                                    </BarChart>
                                </ResponsiveContainer>
                            ) : (
                                <div className="text-gray-400 text-center">No complexity data available</div>
                            )}
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}
