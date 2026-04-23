import { useState, useEffect } from 'react';
import { api } from './api/client';
import TaskForm from './components/TaskForm';
import TaskList from './components/TaskList';
import './App.css';

function App() {
  const [tasks, setTasks] = useState([]);
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchData = async () => {
    try {
      const [tasksRes, catsRes] = await Promise.all([
        api.get('/tasks/'),
        api.get('/categories/')
      ]);
      setTasks(tasksRes.data);
      setCategories(catsRes.data);
    } catch (err) {
      console.error("Ошибка загрузки данных:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { fetchData(); }, []);

  if (loading) return <div className="container"><p className="info">⏳ Загрузка...</p></div>;

  return (
    <div className="container">
      <h1>TaskFlow 📝</h1>
      <TaskForm categories={categories} onTaskCreated={fetchData} />
      <TaskList tasks={tasks} onTaskUpdated={fetchData} />
    </div>
  );
}

export default App;