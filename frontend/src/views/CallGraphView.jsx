import { useCallback, useEffect, useState } from 'react';
import ReactFlow, {
    Background,
    Controls,
    useNodesState,
    useEdgesState,
    addEdge
} from 'react-flow-renderer';
import axios from 'axios';

const nodeTypes = {}; // Custom types if needed

export default function CallGraphView({ projectId }) {
    const [nodes, setNodes, onNodesChange] = useNodesState([]);
    const [edges, setEdges, onEdgesChange] = useEdgesState([]);

    useEffect(() => {
        axios.get(`${import.meta.env.VITE_API_URL || 'http://localhost:8000'}/api/analyze/python/${projectId}`)
            .then(res => {
                const apiNodes = res.data.nodes.map((n, i) => ({
                    id: n.id,
                    data: { label: n.label },
                    position: { x: (i % 5) * 200, y: Math.floor(i / 5) * 100 }, // Simple layout
                    type: 'default',
                    style: {
                        background: '#1e293b',
                        color: '#fff',
                        border: '1px solid #38bdf8',
                        borderRadius: '8px',
                        padding: '10px'
                    }
                }));

                const apiEdges = res.data.edges.map((e, i) => ({
                    id: `e${i}`,
                    source: e.source,
                    target: e.target,
                    animated: true,
                    style: { stroke: '#818cf8' }
                }));

                setNodes(apiNodes);
                setEdges(apiEdges);
            })
            .catch(err => console.error(err));
    }, [projectId]);

    const onConnect = useCallback((params) => setEdges((eds) => addEdge(params, eds)), [setEdges]);

    return (
        <div className="space-y-6 h-[calc(100vh-150px)]">
            <h2 className="text-2xl font-bold">Interactive Call Graph</h2>
            <div className="glass rounded-2xl h-full overflow-hidden border border-white/10">
                <ReactFlow
                    nodes={nodes}
                    edges={edges}
                    onNodesChange={onNodesChange}
                    onEdgesChange={onEdgesChange}
                    onConnect={onConnect}
                    fitView
                >
                    <Background color="#aaa" gap={16} />
                    <Controls />
                </ReactFlow>
            </div>
        </div>
    );
}
