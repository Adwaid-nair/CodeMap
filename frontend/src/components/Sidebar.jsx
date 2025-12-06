import { Link, useLocation, useNavigate } from 'react-router-dom';
import { LayoutDashboard, GitGraph, Network, UploadCloud, Layers } from 'lucide-react';
import clsx from 'clsx';

const NavItem = ({ to, icon: Icon, label, active, disabled }) => (
    <Link
        to={disabled ? '#' : to}
        className={clsx(
            "flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-200",
            active ? "bg-primary/20 text-primary" : "text-gray-400 hover:bg-white/5 hover:text-gray-200",
            disabled && "opacity-50 cursor-not-allowed pointer-events-none"
        )}
    >
        <Icon size={20} />
        <span className="font-medium">{label}</span>
    </Link>
);

export default function Sidebar({ projectId, onNewUpload }) {
    const location = useLocation();
    const navigate = useNavigate();

    const handleNewUpload = () => {
        if (onNewUpload) onNewUpload();
        navigate('/');
    };

    return (
        <aside className="w-64 glass border-r border-white/10 h-full flex flex-col p-4">
            <div className="flex items-center gap-2 px-4 py-4 mb-8">
                <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-primary to-accent"></div>
                <span className="text-xl font-bold tracking-tight">CodeMap</span>
            </div>

            <nav className="flex-1 space-y-2">
                {!projectId && (
                    <div className="px-4 py-2 text-sm text-yellow-500 bg-yellow-500/10 rounded-lg mb-4">
                        Upload a project to start
                    </div>
                )}

                <NavItem
                    to="/"
                    icon={LayoutDashboard}
                    label="Dashboard"
                    active={location.pathname === '/'}
                    disabled={!projectId}
                />
                <NavItem
                    to="/flowchart"
                    icon={Network}
                    label="Flowcharts"
                    active={location.pathname === '/flowchart'}
                    disabled={!projectId}
                />
                <NavItem
                    to="/callgraph"
                    icon={GitGraph}
                    label="Call Graph"
                    active={location.pathname === '/callgraph'}
                    disabled={!projectId}
                />
                <NavItem
                    to="/deps"
                    icon={Layers}
                    label="Dependencies"
                    active={location.pathname === '/deps'}
                    disabled={!projectId}
                />
            </nav>

            <div className="mt-auto pt-8 border-t border-white/10">
                <button onClick={handleNewUpload} className="flex items-center gap-2 px-4 py-2 text-sm text-gray-400 hover:text-white transition-colors">
                    <UploadCloud size={16} />
                    New Upload
                </button>
            </div>
        </aside>
    );
}
