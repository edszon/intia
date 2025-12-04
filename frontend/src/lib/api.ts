// Detecta a URL base dinamicamente
function getApiUrl(): string {
  if (typeof window !== 'undefined') {
    const protocol = window.location.protocol;
    const host = window.location.host;
    // Se estiver rodando em dev (localhost:5173 ou similar), usa backend local
    if (host.includes('localhost') || host.includes('127.0.0.1')) {
      return "http://localhost:8000/api";
    }
    // Caso contrário, assume que o backend está no mesmo host
    return `${protocol}//${host}/api`;
  }
  return import.meta.env.PUBLIC_API_URL || "http://localhost:8000/api";
}

const API_URL = getApiUrl()

export interface Person {
  id: number;
  name: string;
  pfp_image: string | null;
  average_score?: number | null;
}

export async function getPersons(): Promise<Person[]> {
  const res = await fetch(`${API_URL}/persons/`);
  if (!res.ok) throw new Error(`Failed to fetch persons: ${res.statusText}`);
  return res.json();
}

export async function getPersonById(id: number): Promise<Person> {
  const res = await fetch(`${API_URL}/persons/${id}`);
  if (!res.ok) throw new Error(`Failed to fetch person: ${res.statusText}`);
  return res.json();
}

export async function createPerson(name: string, file: File): Promise<Person> {
  const form = new FormData();
  form.append('name', name);
  form.append('file', file);
  const res = await fetch(`${API_URL}/persons`, { method: 'POST', body: form });
  if (!res.ok) throw new Error(`Falha ao criar pessoa: ${res.statusText}`);
  return res.json();
}

export async function updatePerson(personId: number, name?: string, file?: File): Promise<Person> {
  const form = new FormData();
  if (name !== undefined) form.append('name', name);
  if (file) form.append('file', file);
  const res = await fetch(`${API_URL}/persons/${personId}`, { method: 'PUT', body: form });
  if (!res.ok) throw new Error(`Falha ao atualizar pessoa: ${res.statusText}`);
  return res.json();
}

export async function deletePerson(personId: number): Promise<void> {
  const res = await fetch(`${API_URL}/persons/${personId}`, { method: 'DELETE' });
  if (!res.ok) throw new Error(`Falha ao remover pessoa: ${res.statusText}`);
}

export interface Message {
  id: number;
  message: string;
  message_score: number;
  person_id: number;
}

export async function getMessages(personId?: number): Promise<Message[]> {
  const url = personId 
    ? `${API_URL}/messages?person_id=${personId}`
    : `${API_URL}/messages`;
  const res = await fetch(url);
  if (!res.ok) throw new Error(`Failed to fetch messages: ${res.statusText}`);
  return res.json();
}

export async function createMessage(message: string, personId: number): Promise<Message> {
  const res = await fetch(`${API_URL}/messages`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message, person_id: personId })
  });
  if (!res.ok) throw new Error(`Failed to create message: ${res.statusText}`);
  return res.json();
}

export async function previewScore(message: string): Promise<number> {
  const res = await fetch(`${API_URL}/messages/preview-score`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message })
  });
  if (!res.ok) throw new Error(`Failed to preview score: ${res.statusText}`);
  const data = await res.json();
  return data.score;
}

export async function autocomplete(text: string, sliderState: number): Promise<string | null> {
  const res = await fetch(`${API_URL}/messages/autocomplete`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text, slider_state: sliderState })
  });
  if (!res.ok) throw new Error(`Failed to autocomplete: ${res.statusText}`);
  const data = await res.json();
  return (data.suggestion ?? null) as string | null;
}

