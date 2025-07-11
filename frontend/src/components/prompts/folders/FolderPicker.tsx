import React, { useState, useCallback, useMemo } from 'react';
import { FolderOpen, ChevronRight } from 'lucide-react';
import { FolderNavigation } from './FolderNavigation';
import { TemplateFolder } from '@/types/prompts/templates';
import { getMessage } from '@/core/utils/i18n';

interface FolderPickerProps {
  folders: TemplateFolder[];
  onSelect: (folder: TemplateFolder | null, path: string) => void;
  className?: string;
}

type NavState = {
  path: { id: number; title: string }[];
  currentFolder: TemplateFolder | null;
};

export const FolderPicker: React.FC<FolderPickerProps> = ({ folders, onSelect, className = '' }) => {
  const [nav, setNav] = useState<NavState>({ path: [], currentFolder: null });

  const findFolderById = useCallback((list: TemplateFolder[], id?: number): TemplateFolder | null => {
    for (const f of list) {
      if (f.id === id) return f;
      if (f.Folders) {
        const found = findFolderById(f.Folders, id);
        if (found) return found;
      }
    }
    return null;
  }, []);

  const navigateToFolder = useCallback(
    (folder: TemplateFolder) => {
      const newPath = [...nav.path, { id: folder.id, title: folder.title ?? '' }];
      const pathStr = newPath.map(p => p.title).join(' / ');
      setNav({ path: newPath, currentFolder: folder });
      onSelect(folder, pathStr);
    },
    [nav.path, onSelect]
  );

  const navigateBack = useCallback(() => {
    setNav(prev => {
      const newPath = prev.path.slice(0, -1);
      const newCurrent = findFolderById(folders, newPath[newPath.length - 1]?.id);
      const pathStr = newPath.map(p => p.title).join(' / ');
      onSelect(newCurrent, pathStr);
      return { path: newPath, currentFolder: newCurrent };
    });
  }, [folders, findFolderById, onSelect]);

  const navigateToRoot = useCallback(() => {
    setNav({ path: [], currentFolder: null });
    onSelect(null, '');
  }, [onSelect]);

  const navigateToPath = useCallback(
    (index: number) => {
      const newPath = nav.path.slice(0, index + 1);
      const newCurrent = findFolderById(folders, newPath[newPath.length - 1]?.id);
      const pathStr = newPath.map(p => p.title).join(' / ');
      setNav({ path: newPath, currentFolder: newCurrent });
      onSelect(newCurrent, pathStr);
    },
    [nav.path, folders, findFolderById, onSelect]
  );

  const currentFolders = useMemo(() => {
    return nav.currentFolder ? nav.currentFolder.Folders || [] : folders;
  }, [nav.currentFolder, folders]);


  return (
    <div className={`jd-space-y-2 ${className}`}>
      <FolderNavigation
        path={nav.path}
        onNavigateToRoot={navigateToRoot}
        onNavigateBack={navigateBack}
        onNavigateToPath={navigateToPath}
      />
      <div className="jd-space-y-1 jd-max-h-56 jd-overflow-y-auto jd-px-2">
        {currentFolders.map(folder => (
          <div
            key={folder.id}
            className="jd-group jd-flex jd-items-center jd-p-2 jd-rounded-sm hover:jd-bg-accent/60 jd-cursor-pointer"
            onClick={() => navigateToFolder(folder)}
          >
            <FolderOpen className="jd-h-4 jd-w-4 jd-mr-2 jd-text-muted-foreground" />
            <span className="jd-text-sm jd-flex-1 jd-truncate">{folder.title}</span>
            <ChevronRight className="jd-h-3 jd-w-3 jd-text-muted-foreground" />
          </div>
        ))}
        {currentFolders.length === 0 && (
          <div className="jd-text-xs jd-text-muted-foreground jd-p-2">
            {getMessage('noSubfolders', undefined, 'No subfolders')}
          </div>
        )}
      </div>
    </div>
  );
};

export default FolderPicker;
