import { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { Upload, FileCode, CheckCircle2 } from 'lucide-react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

export default function UploadZone({ onUploadComplete }) {
    const [uploading, setUploading] = useState(false);
    const [error, setError] = useState(null);
    const navigate = useNavigate();

    const onDrop = useCallback(async (acceptedFiles) => {
        if (acceptedFiles.length === 0) return;

        const file = acceptedFiles[0];
        setUploading(true);
        setError(null);

        const formData = new FormData();
        formData.append('file', file);

        try {
            // Assuming Backend runs on port 8000
            const response = await axios.post(`${import.meta.env.VITE_API_URL || 'http://localhost:8000'}/upload`, formData, {
                headers: { 'Content-Type': 'multipart/form-data' },
            });

            onUploadComplete(response.data.project_id);
            navigate('/');
        } catch (err) {
            const msg = err.response?.data?.message || err.message || "Upload failed";
            setError(`Upload Error: ${msg}. Check console for details.`);
            console.error("Upload failed:", err);
        } finally {
            setUploading(false);
        }
    }, [onUploadComplete]);

    const { getRootProps, getInputProps, isDragActive } = useDropzone({
        onDrop,
        onDropRejected: (fileRejections) => {
            const msg = fileRejections.map(r => `${r.file.name}: ${r.errors.map(e => e.message).join(', ')}`).join('\n');
            setError(`File rejected:\n${msg}`);
        },
        accept: {
            'application/zip': ['.zip', '.rar', '.7z'],
            'application/x-tar': ['.tar', '.gz'],
            // For simple single file tests
            'text/x-python': ['.py'],
            'text/java': ['.java'],
            'text/x-c++src': ['.cpp', '.h', '.hpp'],
            'text/javascript': ['.js', '.jsx'], // Adding JS/JSX support as it might be common
            'application/javascript': ['.js', '.jsx']
        }
    });

    return (
        <div className="w-full max-w-2xl mx-auto mt-20">
            <div
                {...getRootProps()}
                className={`
          relative overflow-hidden rounded-3xl border-2 border-dashed transition-all duration-300 cursor-pointer
          flex flex-col items-center justify-center p-16
          ${isDragActive ? 'border-primary bg-primary/10' : 'border-white/20 hover:border-white/40 hover:bg-white/5'}
        `}
            >
                <input {...getInputProps()} />

                <div className="bg-surface p-4 rounded-full mb-6 shadow-xl shadow-black/20">
                    {uploading ? (
                        <div className="h-8 w-8 border-2 border-primary border-t-transparent rounded-full animate-spin" />
                    ) : (
                        <Upload className="h-8 w-8 text-primary" />
                    )}
                </div>

                <h3 className="text-2xl font-bold mb-2">
                    {uploading ? 'Analyzing Codebase...' : 'Upload Source Code'}
                </h3>
                <p className="text-gray-400 text-center max-w-sm">
                    Drag and drop your project ZIP file or individual source files here to begin analysis.
                </p>

                {error && (
                    <div className="mt-6 px-4 py-2 bg-red-500/20 text-red-300 rounded-lg text-sm">
                        {error}
                    </div>
                )}
            </div>

            <div className="mt-8 grid grid-cols-3 gap-4">
                {['Python', 'Java', 'C++'].map(lang => (
                    <div key={lang} className="glass p-4 rounded-xl flex items-center gap-3 justify-center">
                        <FileCode size={18} className="text-gray-400" />
                        <span className="text-sm font-medium text-gray-300">{lang}</span>
                    </div>
                ))}
            </div>
        </div>
    );
}
