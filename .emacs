(setq max-specpdl-size 5000)

(setq initial-scratch-message ";; scratch ;;

")

;; server: gnuserv
;; http://www.emacswiki.org/emacs/GnuClient
(if (boundp 'gnuserv-start) (gnuserv-start))
;; frames: http://www.emacswiki.org/emacs/GnuClient#toc6
(setq gnuserv-frame (selected-frame))

;; ;; ;; emacs server (what a piece of crap)
;; (require 'server)
;;   (unless (server-running-p)
;;     (server-start))
;; ;; ;; An error has occurred while loading `/home/jhammel/.emacs':
;; ;; ;; Symbol's function definition is void: server-running-p
;; ;; ;; To ensure normal operation, you should investigate and remove the
;; ;; ;; cause of the error in your initialization file.  Start Emacs with
;; ;; ;; the `--debug-init' option to view a complete error backtrace.

;; ;; ;; For information about GNU Emacs and the GNU system, type C-h C-a.
;; ;; How to fix:
;; http://stackoverflow.com/questions/9999320/how-to-check-if-a-function-e-g-server-running-p-is-available-under-emacs

;;;; bars

;; Turn off the status bar and on the mouse if we're not in a window system
(menu-bar-mode (if window-system 1 -1))

;; no need for a tool bar
(if (boundp 'tool-bar-mode) (tool-bar-mode 0))

;; ...or a startup message
;; instead, it'd be nice to start with a list of recent files (recentf)
(setq inhibit-startup-message t)

;; no f-ing backup files
(setq make-backup-files nil)

;; show trailing whitespace
(setq-default show-trailing-whitespace t)

;;;; ??? no idea

(put 'downcase-region 'disabled nil)
(setq truncate-lines nil)
(setq truncate-partial-width-windows nil)
(setq use-file-dialog nil)

;; make directories when they don't exist
;; from http://stackoverflow.com/questions/6830671/how-to-make-emacs-create-intermediate-dirs-when-saving-a-file
(add-hook 'before-save-hook
          (lambda ()
            (when buffer-file-name
              (let ((dir (file-name-directory buffer-file-name)))
                (when (not (file-exists-p dir))
                  (make-directory dir t))))))

;;;; indentation

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

;;;; line/col #s
;;;; Show line and column numbers in the mode line
(line-number-mode 1)
(column-number-mode 1)


;;;; modes

;; Bind major editing modes to certain file extensions
(setq auto-mode-alist (cons '("\\.zcml$" . sgml-mode) auto-mode-alist))
(setq auto-mode-alist (cons '("\\.pt$" . sgml-mode) auto-mode-alist))
(setq auto-mode-alist (cons '("\\.cpt$" . sgml-mode) auto-mode-alist))
(setq auto-mode-alist (cons '("\\.cpy$" . python-mode) auto-mode-alist))
(setq auto-mode-alist (cons '("\\.vpy$" . python-mode) auto-mode-alist))

;; set auto-fill for appropriate modes
(add-hook 'text-mode-hook 'turn-on-auto-fill)
(add-hook 'sgml-mode-hook 'turn-off-auto-fill)

;; set the grep command....for some reason
(setq grep-command "grep -liE")


;;;; recent history stuff
(require 'recentf)
(recentf-mode 1)
(setq recentf-max-menu-items 25)
(global-set-key "\C-x\ \C-r" 'recentf-open-files)

;;;; full-steam-ahead-and-damn-the-torpedoes
(defun
  full-steam-ahead-and-damn-the-torpedoes
  (prompt) t)
(defalias 'y-or-n-p
  'full-steam-ahead-and-damn-the-torpedoes)
(defalias 'yes-or-no-p
  'full-steam-ahead-and-damn-the-torpedoes)

(require 'uniquify)
(setq uniquify-buffer-name-style 'post-forward)

;;;;

;; wheel mouse
(global-set-key [mouse-4] 'scroll-down)
(global-set-key [mouse-5] 'scroll-up)

;; substring buffer switching mode
(iswitchb-mode 1)

(global-set-key "\M-g" 'goto-line)

;;;; python

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

(fset 'break "import pdb; pdb.set_trace();\C-a\C-i")
(add-hook 'python-mode-hook
          '(lambda ()
             (local-set-key  [(meta ?p) (meta ?p)] 'break)))

(fset 'pytodo "raise NotImplementedError('TODO') # -> record TODO items")

(fset 'python-file "#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os
import sys

here = os.path.dirname(os.path.realpath(__file__))

def main(args=sys.argv[1:]):

    usage = '%prog [options]'
    parser = argparse.ArgumentParser(usage=usage, description=__doc__)
    parser.add_option('input', nargs='?',
                      type=argparse.FileType('r'), default=sys.stdin,
                      help='input file, or read from stdin if ommitted')
    options = parser.parse_args(args)

if __name__ == '__main__':
    main()")
;; TODO: take directly from MakeItSo

(fset 'python-require "def require(url):
    # http://k0s.org/hg/config/file/68635bbb3d3e/python/require.py
    # import a module from the web
    # url should be like scheme://host.name/path/to/module.py

    import imp
    import os
    import tempfile
    import urllib2
    contents = urllib2.urlopen(url).read()
    filename = url.rsplit('/', 1)[-1]
    module = filename.rsplit('.', 1)[0]
    dest = tempfile.mkstemp(suffix='.py', prefix=module)
    f = file(dest, 'w')
    f.write(contents)
    f.close()
    return imp.load_source(module, dest)
")

(fset 'python-test "#!/usr/bin/env python

import os
import unittest

here = os.path.dirname(os.path.abspath(__file__))

class Test__(unittest.TestCase):
    def test__(self):
        pass

if __name__ == '__main__':
    unittest.main()
")


;;; TODO
; - needless to say, zeitgeist integration
; - http://pedrokroger.net/2010/07/configuring-emacs-as-a-python-ide-2/
