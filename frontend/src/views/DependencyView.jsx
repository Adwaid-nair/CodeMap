import { useEffect, useState } from 'react';
import axios from 'axios';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import ReactFlow, { Background, Controls, useNodesState, useEdgesState } from 'react-flow-renderer';

export default function DependencyView({ projectId }) {
    const [metrics, setMetrics] = useState(null);
    const [loading, setLoading] = useState(true);

    // Graph state
    const [nodes, setNodes, onNodesChange] = useNodesState([]);
    const [edges, setEdges, onEdgesChange] = useEdgesState([]);

    useEffect(() => {
        setLoading(true);
        axios.get(`${import.meta.env.VITE_API_URL || 'http://localhost:8000'}/api/analyze/python/${projectId}`)
            .then(res => {
                // 1. Process Complexity Metrics
                const fileMetrics = res.data.complexity.file_metrics;
                const chartData = Object.entries(fileMetrics).map(([name, value]) => ({
                    name,
                    complexity: value
                }));
                setMetrics(chartData);

                // 2. Process File Dependencies
                const rawNodes = res.data.nodes;
                const rawEdges = res.data.edges;

                // Map node ID -> File
                const nodeToFile = {};
                const fileSet = new Set();

                rawNodes.forEach(n => {
                    if (n.file) {
                        nodeToFile[n.id] = n.file;
                        fileSet.add(n.file);
                    }
                });

                // Create File Nodes
                const files = Array.from(fileSet);
                const fileNodes = files.map((file, i) => ({
                    id: file,
                    data: { label: file },
                    position: { x: (i % 4) * 250, y: Math.floor(i / 4) * 150 },
                    type: 'default',
                    style: {
                        background: '#0f172a',
                        color: '#f8fafc',
                        border: '1px solid #38bdf8',
                        borderRadius: '8px',
                        padding: '12px',
                        width: 180,
                        textAlign: 'center'
                    }
                }));

                // Create File Edges (Aggregate function calls)
                const fileEdgesMap = new Set(); // "fileA->fileB"
                const fileEdges = [];

                rawEdges.forEach(e => {
                    const srcFile = nodeToFile[e.source];
                    const tgtFile = nodeToFile[e.target];

                    if (srcFile && tgtFile && srcFile !== tgtFile) {
                        const edgeId = `${srcFile}->${tgtFile}`;
                        if (!fileEdgesMap.has(edgeId)) {
                            fileEdgesMap.add(edgeId);
                            fileEdges.push({
                                id: `e-${edgeId}`,
                                source: srcFile,
                                target: tgtFile,
                                animated: true,
                                style: { stroke: '#818cf8', strokeWidth: 2 },
                                markerEnd: { type: 'arrowclosed', color: '#818cf8' }
                            });
                        }
                    }
                });

                setNodes(fileNodes);
                setEdges(fileEdges);
            })
            .catch(err => console.error(err))
            .finally(() => setLoading(false));
    }, [projectId, setNodes, setEdges]);

    return (
        <div className="space-y-6">
            <h2 className="text-2xl font-bold">File Complexity & Dependencies</h2>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* Complexity Chart */}
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

                {/* File Dependency Graph */}
                <div className="glass p-8 rounded-2xl min-h-[500px] border border-white/10">
                    <h3 className="text-xl font-semibold mb-6">File Dependencies</h3>
                    {loading ? (
                        <div className="animate-pulse text-gray-400">Loading graph...</div>
                    ) : (
                        <div className="h-[400px] w-full border border-white/5 rounded-xl overflow-hidden bg-slate-900/50">
                            {nodes.length > 0 ? (
                                <ReactFlow
                                    nodes={nodes}
                                    edges={edges}
                                    onNodesChange={onNodesChange}
                                    onEdgesChange={onEdgesChange}
                                    fitView
                                >
                                    <Background color="#ffffff" gap={16} size={1} style={{ opacity: 0.1 }} />
                                    <Controls />
                                </ReactFlow>
                            ) : (
                                <div className="h-full flex items-center justify-center text-gray-400">
                                    No dependencies found
                                </div>
                            )}
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}
