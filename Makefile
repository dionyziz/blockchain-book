SOURCES := $(shell find . -iname '*.tex' -o -iname '*.bib' -o -iname '*.sty' -o -iname '*.cls' -o -ipath '*figures/*.pdf')

.PHONY: all clean clean-aux

all: blockchain-foundations.pdf

blockchain-foundations.pdf: $(SOURCES)
	xelatex --halt-on-error blockchain-foundations.tex
	bibtex blockchain-foundations
	makeindex blockchain-foundations.idx
	makeglossaries blockchain-foundations
	xelatex --halt-on-error blockchain-foundations.tex
	xelatex --halt-on-error blockchain-foundations.tex
	xelatex --halt-on-error blockchain-foundations.tex
	$(MAKE) clean-aux

clean:
	$(MAKE) clean-aux
	rm -Rf latex.out
	rm -Rf blockchain-foundations.pdf

clean-aux:
	rm -f *.aux *.log *.out *.cfg *.glo *.idx *.toc *.ilg *.ind *.lof *.lot *.bbl *.blg *.gls *.cut *.hd *.dvi *.ps *.thm *.rpi *.d *.fls *.pyc *.fdb_latexmk *.sls *.slo *.slg *.glsdefs *.gls *.glg *.glo *.ist
