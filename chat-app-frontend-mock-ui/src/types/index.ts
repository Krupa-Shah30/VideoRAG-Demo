export type ChatMessage = {
    id: string;
    sender: string;
    content: string;
    timestamp: Date;
};

export type User = {
    id: string;
    username: string;
    avatarUrl?: string;
};

export type Theme = 'light' | 'dark';

export interface ChatInputProps {
    onSendMessage: (message: string) => void;
    onAttachFile: () => void;
    models: string[];
}

export interface SidebarProps {
    onNewChat: () => void;
    onLogin: () => void;
}

export interface MainPanelProps {
    messages: ChatMessage[];
    onAction: (action: string) => void;
}

export interface ThemeControlsProps {
    currentTheme: Theme;
    onToggleTheme: () => void;
}

export interface SettingsProps {
    onSaveSettings: (settings: any) => void;
}