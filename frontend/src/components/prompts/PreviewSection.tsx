import React from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Eye, ChevronUp, ChevronDown, Copy, Check } from 'lucide-react';
import { cn } from '@/core/utils/classNames';
import { useThemeDetector } from '@/hooks/useThemeDetector';

interface PreviewSectionProps {
  content: string;
  htmlContent?: string;
  expanded: boolean;
  onToggle: () => void;
  isHtml?: boolean;
}

export const PreviewSection: React.FC<PreviewSectionProps> = ({
  content,
  htmlContent,
  expanded,
  onToggle,
  isHtml = false
}) => {
  const [copied, setCopied] = React.useState(false);
  const isDarkMode = useThemeDetector();
  
  // Use content for line counting (the actual text content)
  const lines = content.split('\n');
  const showToggle = lines.length > 3 || content.length > 300; // Show toggle if many lines OR long content
  
  // For text display
  const displayedText = expanded ? content : lines.slice(0, 3).join('\n');
  
  // For HTML display  
  const displayedHtml = htmlContent
    ? expanded
      ? htmlContent
      : htmlContent.split('<br>').slice(0, 3).join('<br>')
    : undefined;

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(content);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      console.error('Failed to copy content:', err);
    }
  };

  return (
    <div className="jd-border-t jd-pt-4">
      <Card
        className={cn(
          'jd-bg-gradient-to-br',
          isDarkMode ? 'jd-from-gray-800 jd-to-gray-900' : 'jd-from-slate-50 jd-to-slate-100'
        )}
      >
        <CardContent className="jd-p-4">
          <div className="jd-flex jd-items-center jd-justify-between jd-mb-3">
            <h4 className="jd-font-medium jd-flex jd-items-center jd-gap-2">
              Preview
            </h4>
            <div className="jd-flex jd-items-center jd-gap-2">
              <Button
                size="sm"
                variant="ghost"
                onClick={handleCopy}
                className="jd-flex jd-items-center jd-gap-1 jd-text-xs"
                disabled={!content.trim()}
              >
                {copied ? (
                  <>
                    <Check className="jd-h-3 jd-w-3" />
                    Copied!
                  </>
                ) : (
                  <>
                    <Copy className="jd-h-3 jd-w-3" />
                    Copy
                  </>
                )}
              </Button>
              {showToggle && (
                <Button 
                  size="sm" 
                  variant="ghost" 
                  onClick={onToggle} 
                  className="jd-flex jd-items-center jd-gap-1"
                >
                  {expanded ? (
                    <>
                      <ChevronUp className="jd-h-4 jd-w-4" />
                      Collapse
                    </>
                  ) : (
                    <>
                      <ChevronDown className="jd-h-4 jd-w-4" />
                      Expand
                    </>
                  )}
                </Button>
              )}
            </div>
          </div>
          
          <div
            className={cn(
              'jd-rounded-lg jd-p-4 jd-relative jd-border',
              isDarkMode ? 'jd-bg-gray-800 jd-border-gray-700' : 'jd-bg-white jd-border-gray-200',
              expanded ? 'jd-max-h-96 jd-overflow-y-auto' : 'jd-max-h-32 jd-overflow-hidden'
            )}
          >
            {isHtml ? (
              <div
                className="jd-whitespace-pre-wrap jd-text-sm jd-leading-relaxed jd-m-0"
                dangerouslySetInnerHTML={{ 
                  __html: displayedHtml || '<span class="jd-text-muted-foreground jd-italic">Your prompt will appear here...</span>' 
                }}
              />
            ) : (
              <div className="jd-whitespace-pre-wrap jd-text-sm jd-leading-relaxed jd-m-0">
                {displayedText || (
                  <span className="jd-text-muted-foreground jd-italic">Your prompt will appear here...</span>
                )}
              </div>
            )}

            {/* Gradient overlay when collapsed and content is long */}
            {!expanded && showToggle && content && (
              <div
                className={cn(
                  'jd-absolute jd-inset-x-0 jd-bottom-0 jd-h-8 jd-bg-gradient-to-t jd-pointer-events-none jd-rounded-b-lg',
                  isDarkMode ? 'jd-from-gray-800 jd-to-gray-800/0' : 'jd-from-white jd-to-white/0'
                )}
              />
            )}
          </div>
          
          <div className="jd-flex jd-justify-between jd-items-center jd-mt-3 jd-text-xs jd-text-muted-foreground">
            <span>{content.length} characters</span>
            <span>{lines.length} lines</span>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};