import { useEffect, useState } from 'react';
import mermaid from 'mermaid';
import axios from 'axios';

mermaid.initialize({
    startOnLoad: true,
    theme: 'dark',
    securityLevel: 'loose',
});

import { TransformWrapper, TransformComponent } from "react-zoom-pan-pinch";

export default function FlowchartView({ projectId }) {
    const [loading, setLoading] = useState(true);
    const [data, setData] = useState(null);

    useEffect(() => {
        // In real app, fetch /api/project/{id}/flowchart
        // For now, mocking or using analyze endpoint
        const fetchData = async () => {
            try {
                // Using logic: Fetch generic nodes and convert to mermaid syntax locally for MVP
                const res = await axios.get(`${import.meta.env.VITE_API_URL || 'http://localhost:8000'}/api/analyze/python/${projectId}`);
                const { nodes, edges } = res.data;

                // Convert to Mermaid syntax
                let chart = 'graph TD;\n';
                nodes.forEach(n => {
                    // Sanitize ID
                    const safeId = n.id.replace(/[^a-zA-Z0-9]/g, '_');
                    chart += `  ${safeId}["${n.label}"];\n`;
                });
                edges.forEach(e => {
                    const safeSource = e.source.replace(/[^a-zA-Z0-9]/g, '_');
                    const safeTarget = e.target.replace(/[^a-zA-Z0-9]/g, '_');
                    chart += `  ${safeSource} --> ${safeTarget};\n`;
                });

                if (nodes.length === 0) {
                    chart = 'graph TD;\n  Start --> End;';
                }

                setData(chart);
            } catch (e) {
                console.error(e);
            } finally {
                setLoading(false);
            }
        };
        fetchData();
    }, [projectId]);

    useEffect(() => {
        if (data) {
            mermaid.contentLoaded();
        }
    }, [data]);

    return (
        <div className="space-y-6">
            <h2 className="text-2xl font-bold">Function Flowchart</h2>
            <div className="glass rounded-2xl h-[600px] flex items-center justify-center overflow-hidden border border-white/10 relative">
                {loading ? (
                    <div className="animate-pulse text-gray-400">Genering Visualization...</div>
                ) : (
                    <TransformWrapper
                        initialScale={1}
                        initialPositionX={0}
                        initialPositionY={0}
                        imgSelection={false}
                        centerOnInit={true}
                        minScale={0.2}
                        maxScale={4}
                        wheel={{ step: 0.1 }}
                    >
                        <TransformComponent wrapperClass="!w-full !h-full" contentClass="!w-full !h-full flex items-center justify-center">
                            <div className="mermaid w-full h-full flex items-center justify-center [&>svg]:!max-w-none [&>svg]:!w-auto [&>svg]:!h-auto">
                                {data}
                            </div>
                        </TransformComponent>
                    </TransformWrapper>
                )}
            </div>
        </div>
    );
}
