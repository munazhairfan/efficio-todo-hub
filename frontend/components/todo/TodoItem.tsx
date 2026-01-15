import { Todo } from '@/types';
import { Checkbox } from '@/components/ui/checkbox';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Edit, Trash2 } from 'lucide-react';

interface TodoItemProps {
  todo: Todo;
  onToggle: (todo: Todo) => void;
  onDelete: (id: string) => void;
  onEdit: (todo: Todo) => void;
}

export function TodoItem({ todo, onToggle, onDelete, onEdit }: TodoItemProps) {
  return (
    <div
      className={`flex items-center justify-between p-4 border-2 rounded-lg ${
        todo.completed
          ? 'border-confetti bg-confetti/50'
          : 'border-merlot bg-white'
      }`}
    >
      <div className="flex items-center gap-4">
        <Checkbox
          checked={todo.completed}
          onCheckedChange={() => onToggle(todo)}
          className="h-6 w-6 border-2 border-merlot data-[state=checked]:bg-merlot data-[state=checked]:text-white"
        />
        <div>
          <h3 className={`text-lg font-bold ${todo.completed ? 'line-through text-gray-500' : 'text-merlot'}`}>
            {todo.title}
          </h3>
          {todo.description && (
            <p className={`text-sm ${todo.completed ? 'line-through text-gray-500' : 'text-mojo'}`}>
              {todo.description}
            </p>
          )}
          <p className="text-xs text-gray-500">
            {new Date(todo.createdAt).toLocaleDateString()}
          </p>
        </div>
      </div>

      <div className="flex gap-2">
        <Button
          variant="outline"
          size="sm"
          onClick={() => onEdit(todo)}
          className="border-2 border-merlot text-merlot hover:bg-merlot hover:text-white"
        >
          <Edit className="h-4 w-4" />
        </Button>

        <Button
          variant="outline"
          size="sm"
          onClick={() => onDelete(todo.id)}
          className="border-2 border-red-500 text-red-500 hover:bg-red-500 hover:text-white"
        >
          <Trash2 className="h-4 w-4" />
        </Button>

        {todo.completed && (
          <Badge variant="secondary" className="bg-green-100 text-green-800 border-green-200">
            Completed
          </Badge>
        )}
      </div>
    </div>
  );
}