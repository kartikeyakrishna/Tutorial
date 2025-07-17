import { useEffect, useState } from 'react';

export default function Health() {
  const [status, setStatus] = useState<string>('');
  useEffect(() => {
    fetch('/api/health')
      .then(res => res.json())
      .then(data => setStatus(data.status))
      .catch(() => setStatus('error'));
  }, []);
  return (
    <div className="p-8 text-center">
      <h1 className="text-2xl font-bold">Backend Health</h1>
      <p className="mt-4">Status: <span className="font-mono">{status}</span></p>
    </div>
  );
} 