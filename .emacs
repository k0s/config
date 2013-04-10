(require 'server)
(or (server-running-p)
    (server-start))
(if (boundp 'tool-bar-mode) (tool-bar-mode 0))
(setq inhibit-startup-message t)
(setq make-backup-files nil)
(put 'downcase-region 'disabled nil)
(setq truncate-lines nil)
(setq truncate-partial-width-windows nil) 
(setq use-file-dialog nil)

;; indentation

;; python indentation
(setq python-indent 4)
(setq-default py-indent-offset 4)
(setq python-guess-indent nil)

;; javascript indentation: http://www.brgeight.se/downloads/emacs/javascript.el
(setq javascript-indent-level 2)
(setq js-indent-level 2)

(setq-default indent-tabs-mode nil)
(defface extra-whitespace-face '((t (:background "pale green"))) "Used for tabs and such.")

(autoload 'doctest-mode "doctest-mode" "doctest editing mode." t)

(transient-mark-mode 1)

(put 'upcase-region 'disabled nil)
;; Show line-number in the mode line
(line-number-mode 1)

;; Show column-number in the mode line
(column-number-mode 1)

;; Bind major editing modes to certain file extensions 
(setq auto-mode-alist (cons '("\\.zcml$" . sgml-mode) auto-mode-alist))
(setq auto-mode-alist (cons '("\\.pt$" . sgml-mode) auto-mode-alist))
(setq auto-mode-alist (cons '("\\.cpt$" . sgml-mode) auto-mode-alist))
(setq auto-mode-alist (cons '("\\.cpy$" . python-mode) auto-mode-alist))
(setq auto-mode-alist (cons '("\\.vpy$" . python-mode) auto-mode-alist))

;; Turn off the status bar and on the mouse if we're not in a window system
(menu-bar-mode (if window-system 1 -1))
(add-hook 'text-mode-hook 'turn-on-auto-fill)

(add-hook 'sgml-mode-hook 'turn-off-auto-fill)

(setq grep-command "grep -liE")

;; recentf stuff
(require 'recentf)
(recentf-mode 1)
(setq recentf-max-menu-items 25)
(global-set-key "\C-x\ \C-r" 'recentf-open-files)

;; full-steam-ahead-and-damn-the-torpedoes
(defun
  full-steam-ahead-and-damn-the-torpedoes
  (prompt) t)
(defalias 'y-or-n-p
  'full-steam-ahead-and-damn-the-torpedoes)
(defalias 'yes-or-no-p
  'full-steam-ahead-and-damn-the-torpedoes)

(require 'uniquify)
(setq uniquify-buffer-name-style 'post-forward)

;; wheel mouse
(global-set-key [mouse-4] 'scroll-down)
(global-set-key [mouse-5] 'scroll-up)

;; substring buffer switching mode
(iswitchb-mode 1)

(global-set-key "\M-g" 'goto-line)

;; (when (load "flymake" t)
;;   (defun flymake-pyflakes-init ()
;;     (let* ((temp-file (flymake-init-create-temp-buffer-copy
;; 		       'flymake-create-temp-inplace))
;; 	   (local-file (file-relative-name
;; 			temp-file
;; 			(file-name-directory buffer-file-name))))
;;       (list "pyflakes" (list local-file))))
  
;;   (add-to-list 'flymake-allowed-file-name-masks
;; 	       '("\\.py\\'" flymake-pyflakes-init)))

;; (add-hook 'find-file-hook 'flymake-find-file-hook)
(server-start)

(fset 'break "import pdb; pdb.set_trace();\C-a\C-i")
(add-hook 'python-mode-hook
          '(lambda ()
             (local-set-key  [(meta ?p) (meta ?p)] 'break)))

(setq-default show-trailing-whitespace t)
