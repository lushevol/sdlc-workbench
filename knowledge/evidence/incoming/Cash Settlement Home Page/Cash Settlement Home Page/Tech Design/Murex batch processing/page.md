# Background

Refer to requirement:  [UK - Murex -> RATAN cashflow feeding]

# High Level Design

Requirement agreement

1. Murex send batch files from 00:00:00 - 19:00:00, every 2 hours send two file( snapshot && base file)
2. Murex uploading complete will create a complete file
3. File maybe include 45000 records in base file for max size
4. Base file include SNTR status only.

Exceptions

| Exception | Exception Code | Action |
| --- | --- | --- |
| Batch file format error | BatchFileFormatError | Stop processing current file and any further files, waiting murex republish the current one |
| File cashflow count is diff with file name convention count | BatchCountReconError | Stop processing current file and any further files, waiting murex republish the current one |
| Some of cashflow fields is invalid | PaymentValidationError | Stop processing current record, waiting murex republish the payment only |

# Detailed Level Design

## Realtime Processing for UK & DE

## Batch Processing

### Design A

### Design B