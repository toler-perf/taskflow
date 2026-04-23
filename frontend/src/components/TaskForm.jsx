import { useState } from 'react';
import { api } from '../api/client';

export default function TaskForm({ categories, onTaskCreated }) {
    const [title, setTitle] = useState('');
    const [categoryId, setCategoryId] = useState(categories[0]?.id || '');

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!title.trim() || !categoryId) return;
        try {
            await api.post('/tasks/', { title, category_id: Number(categoryId) });
            setTitle('');
            onTaskCreated();
        } catch (err) {
            alert('❌ Ошибка создания задачи');
        }
    };

    if (categories.length === 0) {
        return <p className="info">💡 Создайте первую категорию через Swagger UI (http://localhost:8000/docs), чтобы начать.</p>;
    }

    return (
        <form onSubmit={handleSubmit} className="form">
            <input
                value={title}
                onChange={e => setTitle(e.target.value)}
                placeholder="Название новой задачи"
                required
            />
            <select value={categoryId} onChange={e => setCategoryId(e.target.value)}>
                {categories.map(c => (
                    <option key={c.id} value={c.id}>{c.name}</option>
                ))}
            </select>
            <button type="submit">Добавить</button>
        </form>
    );
}