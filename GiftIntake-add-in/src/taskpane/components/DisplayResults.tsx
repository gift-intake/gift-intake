import React from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip";
import { Badge } from "@/components/ui/badge";
import { ScrollArea } from "@/components/ui/scroll-area";
import {
  Calendar,
  Building,
  DollarSign,
  Clock,
  Phone,
  MapPin,
  User,
  GraduationCap,
  CreditCard,
  Mail,
  Gift,
  Repeat,
  Share2,
  LucideIcon,
} from "lucide-react";
import { components } from "@/lib/api/v1";

type InferenceResponseData = components["schemas"]["InferenceResponseData"];
type ParsedEntity = components["schemas"]["ParsedEntity"];

interface DisplayResultsProps {
  data: InferenceResponseData;
}

// Map entity types to Lucide icons
const ENTITY_ICONS: Record<string, LucideIcon> = {
  Interval: Clock,
  Organization: Building,
  Money: DollarSign,
  Date: Calendar,
  Phone: Phone,
  Address: MapPin,
  Person: User,
  Faculty: GraduationCap,
  PaymentMethod: CreditCard,
  Email: Mail,
  "Gift Type": Gift,
  Frequency: Repeat,
  Distribution: Share2,
};

export default function DisplayResults({ data }: DisplayResultsProps) {
  const { file_name, file_contents, entities } = data;

  // Function to render text with highlighted entities
  const renderHighlightedText = () => {
    // Create a map of character positions to entities
    const entityPositions = entities
      .map(({ entity, value }) => {
        const start = file_contents.indexOf(value);
        return {
          start,
          end: start + value.length,
          entity,
          value,
        };
      })
      .filter((pos) => pos.start !== -1);

    // Sort by position and filter overlapping entities
    entityPositions.sort((a, b) => a.start - b.start);

    const filteredPositions = [];
    let lastEnd = -1;

    for (const pos of entityPositions) {
      if (pos.start >= lastEnd) {
        filteredPositions.push(pos);
        lastEnd = pos.end;
      }
    }

    // Build highlighted text elements
    const result = [];
    let currentIndex = 0;

    filteredPositions.forEach((pos, idx) => {
      // Add text before this entity
      if (currentIndex < pos.start) {
        result.push(
          <span key={`text-${idx}`} className="text-gray-700">
            {file_contents.substring(currentIndex, pos.start)}
          </span>
        );
      }

      // Add the highlighted entity with tooltip
      const IconComponent = ENTITY_ICONS[pos.entity];

      result.push(
        <TooltipProvider key={`entity-${idx}`}>
          <Tooltip>
            <TooltipTrigger asChild>
              <span className="inline-flex items-center border border-blue-200 rounded bg-blue-50 px-1.5 py-0.5 mx-0.5">
                {IconComponent && <IconComponent className="inline mr-1" size={14} />}
                {pos.value}
              </span>
            </TooltipTrigger>
            <TooltipContent className="bg-white border border-gray-200 rounded-lg shadow-md px-3 py-1 text-sm text-gray-800 transition-opacity duration-200">
              <p>{pos.entity}</p>
            </TooltipContent>
          </Tooltip>
        </TooltipProvider>
      );

      currentIndex = pos.end;
    });

    // Add remaining text
    if (currentIndex < file_contents.length) {
      result.push(
        <span key="text-end" className="text-gray-700">
          {file_contents.substring(currentIndex)}
        </span>
      );
    }

    return result;
  };

  // Create a legend of entity types using Badge component
  const renderEntityLegend = () => (
    <div className="flex flex-wrap gap-2 mt-4 pt-4 border-t">
      {Object.entries(ENTITY_ICONS).map(([entity, Icon]) => (
        <Badge key={entity} variant="outline" className="flex items-center gap-1.5 px-3 py-1">
          <Icon size={14} />
          {entity}
        </Badge>
      ))}
    </div>
  );

  return (
    <Card>
      <CardHeader>
        <CardTitle>Results</CardTitle>
        {file_name && <CardDescription>{file_name}</CardDescription>}
      </CardHeader>

      <CardContent className="space-y-4">
        <ScrollArea className="max-h-[300px] sm:max-h-[400px] md:max-h-[500px] p-4 border rounded-md">
          <div>{renderHighlightedText()}</div>
        </ScrollArea>

        {/* {renderEntityLegend()} */}
      </CardContent>
    </Card>
  );
}
