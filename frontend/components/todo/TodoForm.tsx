import { useState } from 'react';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Plus } from 'lucide-react';

interface TodoFormProps {
  onSubmit: (title: string, description: string) => void;
  placeholder?: string;
}

export function TodoForm({ onSubmit, placeholder = "What needs to be done?" }: TodoFormProps) {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (title.trim()) {
      onSubmit(title, description);
      setTitle('');
      setDescription('');
    }
  };

  return (
    <form onSubmit={handleSubmit} className="flex gap-4">
      <div className="flex-grow space-y-2">
        <Input
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder={placeholder}
          className="h-12 border-2 border-merlot text-lg rounded-lg px-4"
        />
        <Input
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          placeholder="Add a description (optional)"
          className="h-10 border-2 border-merlot text-base rounded-lg px-4"
        />
      </div>
      <Button
        type="submit"
        className="h-12 bg-mojo hover:bg-merlot text-white font-black text-lg border-2 border-black shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] hover:translate-x-[2px] hover:translate-y-[2px] hover:shadow-none transition-all rounded-xl"
      >
        <Plus className="mr-2 h-5 w-5" />
        Add
      </Button>
    </form>
  );
}