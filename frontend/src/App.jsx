import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Sidebar from './components/Sidebar';
import UploadZone from './components/UploadZone';
import Dashboard from './views/Dashboard';
import FlowchartView from './views/FlowchartView';
import CallGraphView from './views/CallGraphView';
import DependencyView from './views/DependencyView';
import { useState } from 'react';

function App() {
    const [projectId, setProjectId] = useState(null);

    return (
        <Router>
            <div className="flex h-screen bg-background text-gray-100 overflow-hidden">
                <Sidebar projectId={projectId} />

                <main className="flex-1 overflow-auto p-8 relative">
                    <div className="max-w-7xl mx-auto space-y-8">
                        <header className="mb-8">
                            <h1 className="text-3xl font-bold bg-gradient-to-r from-primary to-secondary bg-clip-text text-transparent">
                                CodeMap <span className="text-sm font-normal text-gray-400">Intelligent Analysis</span>
                            </h1>
                        </header>

                        {!projectId ? (
                            <UploadZone onUploadComplete={setProjectId} />
                        ) : (
                            <Routes>
                                <Route path="/" element={<Dashboard projectId={projectId} />} />
                                <Route path="/flowchart" element={<FlowchartView projectId={projectId} />} />
                                <Route path="/callgraph" element={<CallGraphView projectId={projectId} />} />
                                <Route path="/deps" element={<DependencyView projectId={projectId} />} />
                                <Route path="*" element={<Navigate to="/" />} />
                            </Routes>
                        )}
                    </div>
                </main>
            </div>
        </Router>
    );
}

export default App;
