struct FontInfo;

extern const struct FontInfo sFontInfos[];
extern const struct FontInfo *gFonts;

void SetFontsPointer(const struct FontInfo *fonts)
{
    gFonts = fonts;
}

void SetDefaultFontsPointer(void)
{
    SetFontsPointer(sFontInfos);
}
