// src/components/ui/card.tsx

import React, { forwardRef } from 'react';
import { cn } from '@/core/utils/classNames';

export interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
  variant?: 'default' | 'bordered' | 'elevated' | 'ghost';
}

export const Card = forwardRef<HTMLDivElement, CardProps>(
  ({ className, variant = 'default', ...props }, ref) => {
    // Base classes
    const baseClasses = 'jd-rounded-lg';
    
    // Variant classes
    const variantClasses = {
      default: 'jd-bg-background jd-text-card-foreground jd-shadow',
      bordered: 'jd-bg-background jd-text-card-foreground jd-border jd-border-border',
      elevated: 'jd-bg-background jd-text-card-foreground jd-shadow-lg',
      ghost: 'jd-bg-transparent jd-text-card-foreground',
    };
    
    return (
      <div
        ref={ref}
        className={cn(
          baseClasses,
          variantClasses[variant],
          className
        )}
        {...props}
      />
    );
  }
);

Card.displayName = 'Card';

export interface CardHeaderProps extends React.HTMLAttributes<HTMLDivElement> {}

export const CardHeader = forwardRef<HTMLDivElement, CardHeaderProps>(
  ({ className, ...props }, ref) => (
    <div
      ref={ref}
      className={cn('jd-flex jd-flex-col jd-space-y-1.5 jd-p-6', className)}
      {...props}
    />
  )
);

CardHeader.displayName = 'CardHeader';

export interface CardTitleProps extends React.HTMLAttributes<HTMLHeadingElement> {
  as?: 'h1' | 'h2' | 'h3' | 'h4' | 'h5' | 'h6';
}

export const CardTitle = forwardRef<HTMLHeadingElement, CardTitleProps>(
  ({ className, as: Tag = 'h3', ...props }, ref) => (
    <Tag
      ref={ref}
      className={cn('jd-font-semibold jd-leading-none jd-tracking-tight', className)}
      {...props}
    />
  )
);

CardTitle.displayName = 'CardTitle';

export interface CardDescriptionProps extends React.HTMLAttributes<HTMLParagraphElement> {}

export const CardDescription = forwardRef<HTMLParagraphElement, CardDescriptionProps>(
  ({ className, ...props }, ref) => (
    <p
      ref={ref}
      className={cn('jd-text-sm jd-text-muted-foreground', className)}
      {...props}
    />
  )
);

CardDescription.displayName = 'CardDescription';

export interface CardContentProps extends React.HTMLAttributes<HTMLDivElement> {
  paddingless?: boolean;
}

export const CardContent = forwardRef<HTMLDivElement, CardContentProps>(
  ({ className, paddingless = false, ...props }, ref) => (
    <div
      ref={ref}
      className={cn(paddingless ? '' : 'jd-p-6 jd-pt-0', className)}
      {...props}
    />
  )
);

CardContent.displayName = 'CardContent';

export interface CardFooterProps extends React.HTMLAttributes<HTMLDivElement> {}

export const CardFooter = forwardRef<HTMLDivElement, CardFooterProps>(
  ({ className, ...props }, ref) => (
    <div
      ref={ref}
      className={cn('jd-flex jd-items-center jd-p-6 jd-pt-0', className)}
      {...props}
    />
  )
);

CardFooter.displayName = 'CardFooter';