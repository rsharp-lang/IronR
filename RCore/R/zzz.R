
.onLoad <- function(libname, pkgname) {
    netcore5_init0();
}

.flashLoad <- function() .onLoad(NULL, NULL);
