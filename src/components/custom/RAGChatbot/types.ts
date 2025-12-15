export interface ChatMessage {
  type: 'user' | 'bot';
  text: string;
  sources?: { url: string; page_title: string; chunk_index: number; content: string }[];
}
