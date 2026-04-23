import { api } from '../api/client';

export default function TaskList({ tasks, onTaskUpdated }) {
    const toggleStatus = async (task) => {
        const newStatus = task.status === 'done' ? 'todo' : 'done';
        try {
            await api.put(`/tasks/${task.id}/`, { status: newStatus });
            onTaskUpdated();
        } catch (err) {
            alert('❌ Ошибка обновления статуса');
        }
    };

    const deleteTask = async (id) => {
        if (!confirm('Удалить задачу?')) return;
        try {
            await api.delete(`/tasks/${id}/`);
            onTaskUpdated();
        } catch (err) {
            alert('❌ Ошибка удаления');
        }
    };

    if (tasks.length === 0) return <p className="info">🎉 Задач пока нет. Создайте первую!</p>;

    return (
        <ul className="task-list">
            {tasks.map(task => (
                <li key={task.id} className={`task ${task.status === 'done' ? 'done' : ''}`}>
                    <span className="task-title" onClick={() => toggleStatus(task)}>
                        {task.status === 'done' ? '✅' : '⬜'} {task.title}
                    </span>
                    <span className="task-category">📁 {task.category?.name || 'Без категории'}</span>
                    <button className="delete-btn" onClick={() => deleteTask(task.id)}>🗑</button>
                </li>
            ))}
        </ul>
    );
}